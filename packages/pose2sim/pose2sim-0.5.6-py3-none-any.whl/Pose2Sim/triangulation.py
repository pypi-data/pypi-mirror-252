#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
    ###########################################################################
    ## ROBUST TRIANGULATION  OF 2D COORDINATES                               ##
    ###########################################################################
    
    This module triangulates 2D json coordinates and builds a .trc file readable 
    by OpenSim.
    
    The triangulation is weighted by the likelihood of each detected 2D keypoint 
    (if they meet the likelihood threshold). If the reprojection error is above a
    threshold, right and left sides are swapped; if it is still above, a camera 
    is removed for this point and this frame, until the threshold is met. If more 
    cameras are removed than a predefined minimum, triangulation is skipped for 
    the point and this frame. In the end, missing values are interpolated.

    In case of multiple subjects detection, make sure you first run the 
    personAssociation module.

    INPUTS: 
    - a calibration file (.toml extension)
    - json files for each camera with only one person of interest
    - a Config.toml file
    - a skeleton model
    
    OUTPUTS: 
    - a .trc file with 3D coordinates in Y-up system coordinates
    
'''


## INIT
import os
import glob
import fnmatch
import numpy as np
import json
import itertools as it
import pandas as pd
import cv2
import toml
from tqdm import tqdm
from scipy import interpolate
from collections import Counter
from anytree import RenderTree
from anytree.importer import DictImporter
import logging

from Pose2Sim.common import retrieve_calib_params, computeP, weighted_triangulation, \
    reprojection, euclidean_distance, natural_sort
from Pose2Sim.skeletons import *


## AUTHORSHIP INFORMATION
__author__ = "David Pagnon"
__copyright__ = "Copyright 2021, Pose2Sim"
__credits__ = ["David Pagnon"]
__license__ = "BSD 3-Clause License"
__version__ = '0.4'
__maintainer__ = "David Pagnon"
__email__ = "contact@david-pagnon.com"
__status__ = "Development"


## FUNCTIONS
def zup2yup(Q):
    '''
    Turns Z-up system coordinates into Y-up coordinates

    INPUT:
    - Q: pandas dataframe
    N 3D points as columns, ie 3*N columns in Z-up system coordinates
    and frame number as rows

    OUTPUT:
    - Q: pandas dataframe with N 3D points in Y-up system coordinates
    '''
    
    # X->Y, Y->Z, Z->X
    cols = list(Q.columns)
    cols = np.array([[cols[i*3+1],cols[i*3+2],cols[i*3]] for i in range(int(len(cols)/3))]).flatten()
    Q = Q[cols]

    return Q


def interpolate_zeros_nans(col, *args):
    '''
    Interpolate missing points (of value zero),
    unless more than N contiguous values are missing.

    INPUTS:
    - col: pandas column of coordinates
    - args[0] = N: max number of contiguous bad values, above which they won't be interpolated
    - args[1] = kind: 'linear', 'slinear', 'quadratic', 'cubic'. Default: 'cubic'

    OUTPUT:
    - col_interp: interpolated pandas column
    '''

    if len(args)==2:
        N, kind = args
    if len(args)==1:
        N = np.inf
        kind = args[0]
    if not args:
        N = np.inf
    
    # Interpolate nans
    mask = ~(np.isnan(col) | col.eq(0)) # true where nans or zeros
    idx_good = np.where(mask)[0]
    if 'kind' not in locals(): # 'linear', 'slinear', 'quadratic', 'cubic'
        f_interp = interpolate.interp1d(idx_good, col[idx_good], kind="linear", bounds_error=False)
    else:
        f_interp = interpolate.interp1d(idx_good, col[idx_good], kind=kind, fill_value='extrapolate', bounds_error=False)
    col_interp = np.where(mask, col, f_interp(col.index)) #replace at false index with interpolated values
    
    # Reintroduce nans if lenght of sequence > N
    idx_notgood = np.where(~mask)[0]
    gaps = np.where(np.diff(idx_notgood) > 1)[0] + 1 # where the indices of true are not contiguous
    sequences = np.split(idx_notgood, gaps)
    if sequences[0].size>0:
        for seq in sequences:
            if len(seq) > N: # values to exclude from interpolation are set to false when they are too long 
                col_interp[seq] = np.nan
    
    return col_interp


def make_trc(config, Q, keypoints_names, f_range):
    '''
    Make Opensim compatible trc file from a dataframe with 3D coordinates

    INPUT:
    - config: dictionary of configuration parameters
    - Q: pandas dataframe with 3D coordinates as columns, frame number as rows
    - keypoints_names: list of strings
    - f_range: list of two numbers. Range of frames

    OUTPUT:
    - trc file
    '''

    # Read config
    project_dir = config.get('project').get('project_dir')
    frame_rate = config.get('project').get('frame_rate')
    seq_name = os.path.basename(os.path.realpath(project_dir))
    pose3d_dir = os.path.join(project_dir, 'pose-3d')

    trc_f = f'{seq_name}_{f_range[0]}-{f_range[1]}.trc'

    #Header
    DataRate = CameraRate = OrigDataRate = frame_rate
    NumFrames = len(Q)
    NumMarkers = len(keypoints_names)
    header_trc = ['PathFileType\t4\t(X/Y/Z)\t' + trc_f, 
            'DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames', 
            '\t'.join(map(str,[DataRate, CameraRate, NumFrames, NumMarkers, 'm', OrigDataRate, f_range[0], f_range[1]])),
            'Frame#\tTime\t' + '\t\t\t'.join(keypoints_names) + '\t\t',
            '\t\t'+'\t'.join([f'X{i+1}\tY{i+1}\tZ{i+1}' for i in range(len(keypoints_names))])]
    
    # Zup to Yup coordinate system
    Q = zup2yup(Q)
    
    #Add Frame# and Time columns
    Q.index = np.array(range(0, f_range[1]-f_range[0])) + 1
    Q.insert(0, 't', Q.index / frame_rate)

    #Write file
    if not os.path.exists(pose3d_dir): os.mkdir(pose3d_dir)
    trc_path = os.path.realpath(os.path.join(pose3d_dir, trc_f))
    with open(trc_path, 'w') as trc_o:
        [trc_o.write(line+'\n') for line in header_trc]
        Q.to_csv(trc_o, sep='\t', index=True, header=None, lineterminator='\n')

    return trc_path


def recap_triangulate(config, error, nb_cams_excluded, keypoints_names, cam_excluded_count, interp_frames, non_interp_frames, trc_path):
    '''
    Print a message giving statistics on reprojection errors (in pixel and in m)
    as well as the number of cameras that had to be excluded to reach threshold 
    conditions. Also stored in User/logs.txt.

    INPUT:
    - a Config.toml file
    - error: dataframe 
    - nb_cams_excluded: dataframe
    - keypoints_names: list of strings

    OUTPUT:
    - Message in console
    '''

    # Read config
    project_dir = config.get('project').get('project_dir')
    session_dir = os.path.realpath(os.path.join(project_dir, '..', '..'))
    calib_dir = [os.path.join(session_dir, c) for c in os.listdir(session_dir) if ('Calib' or 'calib') in c][0]
    calib_file = glob.glob(os.path.join(calib_dir, '*.toml'))[0] # lastly created calibration file
    calib = toml.load(calib_file)
    cam_names = np.array([calib[c].get('name') for c in list(calib.keys())])
    cam_names = cam_names[list(cam_excluded_count.keys())]
    error_threshold_triangulation = config.get('triangulation').get('reproj_error_threshold_triangulation')
    likelihood_threshold = config.get('triangulation').get('likelihood_threshold_triangulation')
    show_interp_indices = config.get('triangulation').get('show_interp_indices')
    interpolation_kind = config.get('triangulation').get('interpolation')
    handle_LR_swap = config.get('triangulation').get('handle_LR_swap')
    undistort_points = config.get('triangulation').get('undistort_points')
    
    # Recap
    calib_cam1 = calib[list(calib.keys())[0]]
    fm = calib_cam1['matrix'][0][0]
    Dm = euclidean_distance(calib_cam1['translation'], [0,0,0])

    logging.info('')
    for idx, name in enumerate(keypoints_names):
        mean_error_keypoint_px = np.around(error.iloc[:,idx].mean(), decimals=1) # RMS à la place?
        mean_error_keypoint_m = np.around(mean_error_keypoint_px * Dm / fm, decimals=3)
        mean_cam_excluded_keypoint = np.around(nb_cams_excluded.iloc[:,idx].mean(), decimals=2)
        logging.info(f'Mean reprojection error for {name} is {mean_error_keypoint_px} px (~ {mean_error_keypoint_m} m), reached with {mean_cam_excluded_keypoint} excluded cameras. ')
        if show_interp_indices:
            if interpolation_kind != 'none':
                if len(list(interp_frames[idx])) ==0:
                    logging.info(f'  No frames needed to be interpolated.')
                else: 
                    interp_str = str(interp_frames[idx]).replace(":", " to ").replace("'", "").replace("]", "").replace("[", "")
                    logging.info(f'  Frames {interp_str} were interpolated.')
                if len(list(non_interp_frames[idx]))>0:
                    noninterp_str = str(non_interp_frames[idx]).replace(":", " to ").replace("'", "").replace("]", "").replace("[", "")
                    logging.info(f'  Frames {non_interp_frames[idx]} could not be interpolated: consider adjusting thresholds.')
            else:
                logging.info(f'  No frames were interpolated because \'interpolation_kind\' was set to none. ')
    
    mean_error_px = np.around(error['mean'].mean(), decimals=1)
    mean_error_mm = np.around(mean_error_px * Dm / fm *1000, decimals=1)
    mean_cam_excluded = np.around(nb_cams_excluded['mean'].mean(), decimals=2)

    logging.info(f'\n--> Mean reprojection error for all points on all frames is {mean_error_px} px, which roughly corresponds to {mean_error_mm} mm. ')
    logging.info(f'Cameras were excluded if likelihood was below {likelihood_threshold} and if the reprojection error was above {error_threshold_triangulation} px.') 
    logging.info(f'In average, {mean_cam_excluded} cameras had to be excluded to reach these thresholds.')
    cam_excluded_count = {i: v for i, v in zip(cam_names, cam_excluded_count.values())}
    str_cam_excluded_count = ''
    for i, (k, v) in enumerate(cam_excluded_count.items()):
        if i ==0:
             str_cam_excluded_count += f'Camera {k} was excluded {int(np.round(v*100))}% of the time, '
        elif i == len(cam_excluded_count)-1:
            str_cam_excluded_count += f'and Camera {k}: {int(np.round(v*100))}%.'
        else:
            str_cam_excluded_count += f'Camera {k}: {int(np.round(v*100))}%, '
    logging.info(str_cam_excluded_count)
    
    logging.info(f'Limb swapping was {"handled" if handle_LR_swap else "not handled"}.')
    logging.info(f'Lens distortions were {"taken into account" if undistort_points else "not taken into account"}.')

    logging.info(f'\n3D coordinates are stored at {trc_path}.')


def triangulation_from_best_cameras(config, coords_2D_kpt, coords_2D_kpt_swapped, projection_matrices, calib_params):
    '''
    Triangulates 2D keypoint coordinates. If reprojection error is above threshold,
    tries swapping left and right sides. If still above, removes a camera until error
    is below threshold unless the number of remaining cameras is below a predefined number.

    1. Creates subset with N cameras excluded 
    2. Tries all possible triangulations
    3. Chooses the one with smallest reprojection error
    If error too big, take off one more camera.
        If then below threshold, retain result.
        If better but still too big, take off one more camera.
    
    INPUTS:
    - a Config.toml file
    - coords_2D_kpt: (x,y,likelihood) * ncams array
    - coords_2D_kpt_swapped: (x,y,likelihood) * ncams array  with left/right swap
    - projection_matrices: list of arrays

    OUTPUTS:
    - Q: array of triangulated point (x,y,z,1.)
    - error_min: float
    - nb_cams_excluded: int
    '''
    
    # Read config
    error_threshold_triangulation = config.get('triangulation').get('reproj_error_threshold_triangulation')
    min_cameras_for_triangulation = config.get('triangulation').get('min_cameras_for_triangulation')
    handle_LR_swap = config.get('triangulation').get('handle_LR_swap')

    undistort_points = config.get('triangulation').get('undistort_points')
    if undistort_points:
        calib_params_K = calib_params['K']
        calib_params_dist = calib_params['dist']
        calib_params_R = calib_params['R']
        calib_params_T = calib_params['T']

    # Initialize
    x_files, y_files, likelihood_files = coords_2D_kpt
    x_files_swapped, y_files_swapped, likelihood_files_swapped = coords_2D_kpt_swapped
    n_cams = len(x_files)
    error_min = np.inf 
    
    nb_cams_off = 0 # cameras will be taken-off until reprojection error is under threshold
    # print('\n')
    while error_min > error_threshold_triangulation and n_cams - nb_cams_off >= min_cameras_for_triangulation:
        # print("error min ", error_min, "thresh ", error_threshold_triangulation, 'nb_cams_off ', nb_cams_off)
        # Create subsets with "nb_cams_off" cameras excluded
        id_cams_off = np.array(list(it.combinations(range(n_cams), nb_cams_off)))
        
        if undistort_points:
            calib_params_K_filt = [calib_params_K]*len(id_cams_off)
            calib_params_dist_filt = [calib_params_dist]*len(id_cams_off)
            calib_params_R_filt = [calib_params_R]*len(id_cams_off)
            calib_params_T_filt = [calib_params_T]*len(id_cams_off)
        projection_matrices_filt = [projection_matrices]*len(id_cams_off)

        x_files_filt = np.vstack([x_files.copy()]*len(id_cams_off))
        y_files_filt = np.vstack([y_files.copy()]*len(id_cams_off))
        x_files_swapped_filt = np.vstack([x_files_swapped.copy()]*len(id_cams_off))
        y_files_swapped_filt = np.vstack([y_files_swapped.copy()]*len(id_cams_off))
        likelihood_files_filt = np.vstack([likelihood_files.copy()]*len(id_cams_off))
        
        if nb_cams_off > 0:
            for i in range(len(id_cams_off)):
                x_files_filt[i][id_cams_off[i]] = np.nan
                y_files_filt[i][id_cams_off[i]] = np.nan
                x_files_swapped_filt[i][id_cams_off[i]] = np.nan
                y_files_swapped_filt[i][id_cams_off[i]] = np.nan
                likelihood_files_filt[i][id_cams_off[i]] = np.nan
        
        # Excluded cameras index and count
        id_cams_off_tot = [np.argwhere(np.isnan(x)).ravel() for x in likelihood_files_filt]
        nb_cams_excluded_filt = [np.count_nonzero(np.nan_to_num(x)==0) for x in likelihood_files_filt] # count nans and zeros
        nb_cams_off_tot = max(nb_cams_excluded_filt)
        # print('likelihood_files_filt ',likelihood_files_filt)
        # print('nb_cams_excluded_filt ', nb_cams_excluded_filt, 'nb_cams_off_tot ', nb_cams_off_tot)
        if nb_cams_off_tot > n_cams - min_cameras_for_triangulation:
            break
        # print('still in loop')
        if undistort_points:
            calib_params_K_filt = [ [ c[i] for i in range(n_cams) if not np.isnan(likelihood_files_filt[j][i]) and not likelihood_files_filt[j][i]==0. ] for j, c in enumerate(calib_params_K_filt) ]
            calib_params_dist_filt = [ [ c[i] for i in range(n_cams) if not np.isnan(likelihood_files_filt[j][i]) and not likelihood_files_filt[j][i]==0. ] for j, c in enumerate(calib_params_dist_filt) ]
            calib_params_R_filt = [ [ c[i] for i in range(n_cams) if not np.isnan(likelihood_files_filt[j][i]) and not likelihood_files_filt[j][i]==0. ] for j, c in enumerate(calib_params_R_filt) ]
            calib_params_T_filt = [ [ c[i] for i in range(n_cams) if not np.isnan(likelihood_files_filt[j][i]) and not likelihood_files_filt[j][i]==0. ] for j, c in enumerate(calib_params_T_filt) ]
        projection_matrices_filt = [ [ p[i] for i in range(n_cams) if not np.isnan(likelihood_files_filt[j][i]) and not likelihood_files_filt[j][i]==0. ] for j, p in enumerate(projection_matrices_filt) ]
        
        # print('\nnb_cams_off', repr(nb_cams_off), 'nb_cams_excluded', repr(nb_cams_excluded_filt))
        # print('likelihood_files ', repr(likelihood_files))
        # print('y_files ', repr(y_files))
        # print('x_files ', repr(x_files))
        # print('x_files_swapped ', repr(x_files_swapped))
        # print('likelihood_files_filt ', repr(likelihood_files_filt))
        # print('x_files_filt ', repr(x_files_filt))
        # print('id_cams_off_tot ', id_cams_off_tot)
        
        x_files_filt = [ np.array([ xx for ii, xx in enumerate(x) if not np.isnan(likelihood_files_filt[i][ii]) and not likelihood_files_filt[i][ii]==0. ]) for i,x in enumerate(x_files_filt) ]
        y_files_filt = [ np.array([ xx for ii, xx in enumerate(x) if not np.isnan(likelihood_files_filt[i][ii]) and not likelihood_files_filt[i][ii]==0. ]) for i,x in enumerate(y_files_filt) ]
        x_files_swapped_filt = [ np.array([ xx for ii, xx in enumerate(x) if not np.isnan(likelihood_files_filt[i][ii]) and not likelihood_files_filt[i][ii]==0. ]) for i,x in enumerate(x_files_swapped_filt) ]
        y_files_swapped_filt = [ np.array([ xx for ii, xx in enumerate(x) if not np.isnan(likelihood_files_filt[i][ii]) and not likelihood_files_filt[i][ii]==0. ]) for i,x in enumerate(y_files_swapped_filt) ]
        likelihood_files_filt = [ np.array([ xx for ii, xx in enumerate(x) if not np.isnan(xx) and not xx==0. ]) for x in likelihood_files_filt ]
        # print('y_files_filt ', repr(y_files_filt))
        # print('x_files_filt ', repr(x_files_filt))
        # Triangulate 2D points
        Q_filt = [weighted_triangulation(projection_matrices_filt[i], x_files_filt[i], y_files_filt[i], likelihood_files_filt[i]) for i in range(len(id_cams_off))]
        
        # Reprojection
        if undistort_points:
            coords_2D_kpt_calc_filt = [np.array([cv2.projectPoints(np.array(Q_filt[i][:-1]), calib_params_R_filt[i][j], calib_params_T_filt[i][j], calib_params_K_filt[i][j], calib_params_dist_filt[i][j])[0].ravel() 
                                        for j in range(n_cams-nb_cams_excluded_filt[i])]) 
                                        for i in range(len(id_cams_off))]
            coords_2D_kpt_calc_filt = [[coords_2D_kpt_calc_filt[i][:,0], coords_2D_kpt_calc_filt[i][:,1]] for i in range(len(id_cams_off))]
        else:
            coords_2D_kpt_calc_filt = [reprojection(projection_matrices_filt[i], Q_filt[i]) for i in range(len(id_cams_off))]
        coords_2D_kpt_calc_filt = np.array(coords_2D_kpt_calc_filt, dtype=object)
        x_calc_filt = coords_2D_kpt_calc_filt[:,0]
        # print('x_calc_filt ', x_calc_filt)
        y_calc_filt = coords_2D_kpt_calc_filt[:,1]
        
        # Reprojection error
        error = []
        for config_off_id in range(len(x_calc_filt)):
            q_file = [(x_files_filt[config_off_id][i], y_files_filt[config_off_id][i]) for i in range(len(x_files_filt[config_off_id]))]
            q_calc = [(x_calc_filt[config_off_id][i], y_calc_filt[config_off_id][i]) for i in range(len(x_calc_filt[config_off_id]))]
            error.append( np.mean( [euclidean_distance(q_file[i], q_calc[i]) for i in range(len(q_file))] ) )
        # print('error ', error)
            
        # Choosing best triangulation (with min reprojection error)
        error_min = np.nanmin(error)
        # print(error_min)
        best_cams = np.argmin(error)
        nb_cams_excluded = nb_cams_excluded_filt[best_cams]
        
        Q = Q_filt[best_cams][:-1]


        # Swap left and right sides if reprojection error still too high
        if handle_LR_swap and error_min > error_threshold_triangulation:
            n_cams_swapped = 1
            error_off_swap_min = error_min
            while error_off_swap_min > error_threshold_triangulation and n_cams_swapped < (n_cams - nb_cams_off_tot) / 2: # more than half of the cameras switched: may triangulate twice the same side
                # print('SWAP: nb_cams_off ', nb_cams_off, 'n_cams_swapped ', n_cams_swapped, 'nb_cams_off_tot ', nb_cams_off_tot)
                # Create subsets 
                id_cams_swapped = np.array(list(it.combinations(range(n_cams-nb_cams_off_tot), n_cams_swapped)))
                # print('id_cams_swapped ', id_cams_swapped)
                x_files_filt_off_swap = [[x] * len(id_cams_swapped) for x in x_files_filt]
                y_files_filt_off_swap = [[y] * len(id_cams_swapped) for y in y_files_filt]
                # print('x_files_filt_off_swap ', x_files_filt_off_swap)
                # print('y_files_filt_off_swap ', y_files_filt_off_swap)
                for id_off in range(len(id_cams_off)): # for each configuration with nb_cams_off_tot removed 
                    for id_swapped, config_swapped in enumerate(id_cams_swapped): # for each of these configurations, test all subconfigurations with with n_cams_swapped swapped
                        # print('id_off ', id_off, 'id_swapped ', id_swapped, 'config_swapped ',  config_swapped)
                        x_files_filt_off_swap[id_off][id_swapped][config_swapped] = x_files_swapped_filt[id_off][config_swapped] 
                        y_files_filt_off_swap[id_off][id_swapped][config_swapped] = y_files_swapped_filt[id_off][config_swapped]
                                
                # Triangulate 2D points
                Q_filt_off_swap = np.array([[weighted_triangulation(projection_matrices_filt[id_off], x_files_filt_off_swap[id_off][id_swapped], y_files_filt_off_swap[id_off][id_swapped], likelihood_files_filt[id_off]) 
                                                for id_swapped in range(len(id_cams_swapped))]
                                                for id_off in range(len(id_cams_off))] )
                
                # Reprojection
                if undistort_points:
                    coords_2D_kpt_calc_off_swap = [np.array([[cv2.projectPoints(np.array(Q_filt_off_swap[id_off][id_swapped][:-1]), calib_params_R_filt[id_off][j], calib_params_T_filt[id_off][j], calib_params_K_filt[id_off][j], calib_params_dist_filt[id_off][j])[0].ravel() 
                                                    for j in range(n_cams-nb_cams_off_tot)] 
                                                    for id_swapped in range(len(id_cams_swapped))])
                                                    for id_off in range(len(id_cams_off))]
                    coords_2D_kpt_calc_off_swap = np.array([[[coords_2D_kpt_calc_off_swap[id_off][id_swapped,:,0], coords_2D_kpt_calc_off_swap[id_off][id_swapped,:,1]] 
                                                    for id_swapped in range(len(id_cams_swapped))] 
                                                    for id_off in range(len(id_cams_off))])
                else:
                    coords_2D_kpt_calc_off_swap = [np.array([reprojection(projection_matrices_filt[id_off], Q_filt_off_swap[id_off][id_swapped]) 
                                                    for id_swapped in range(len(id_cams_swapped))])
                                                    for id_off in range(len(id_cams_off))]
                # print(repr(coords_2D_kpt_calc_off_swap))
                x_calc_off_swap = [c[:,0] for c in coords_2D_kpt_calc_off_swap]
                y_calc_off_swap = [c[:,1] for c in coords_2D_kpt_calc_off_swap]
                
                # Reprojection error
                # print('x_files_filt_off_swap ', x_files_filt_off_swap)
                # print('x_calc_off_swap ', x_calc_off_swap)
                error_off_swap = []
                for id_off in range(len(id_cams_off)):
                    error_percam = []
                    for id_swapped, config_swapped in enumerate(id_cams_swapped):
                        # print(id_off,id_swapped,n_cams,nb_cams_off)
                        # print(repr(x_files_filt_off_swap))
                        q_file_off_swap = [(x_files_filt_off_swap[id_off][id_swapped][i], y_files_filt_off_swap[id_off][id_swapped][i]) for i in range(n_cams - nb_cams_off_tot)]
                        q_calc_off_swap = [(x_calc_off_swap[id_off][id_swapped][i], y_calc_off_swap[id_off][id_swapped][i]) for i in range(n_cams - nb_cams_off_tot)]
                        error_percam.append( np.mean( [euclidean_distance(q_file_off_swap[i], q_calc_off_swap[i]) for i in range(len(q_file_off_swap))] ) )
                    error_off_swap.append(error_percam)
                error_off_swap = np.array(error_off_swap)
                # print('error_off_swap ', error_off_swap)
                
                # Choosing best triangulation (with min reprojection error)
                error_off_swap_min = np.min(error_off_swap)
                best_off_swap_config = np.unravel_index(error_off_swap.argmin(), error_off_swap.shape)
                
                id_off_cams = best_off_swap_config[0]
                id_swapped_cams = id_cams_swapped[best_off_swap_config[1]]
                Q_best = Q_filt_off_swap[best_off_swap_config][:-1]

                n_cams_swapped += 1

            if error_off_swap_min < error_min:
                error_min = error_off_swap_min
                best_cams = id_off_cams
                Q = Q_best
        
        # print(error_min)
        nb_cams_off += 1
    
    # Index of excluded cams for this keypoint
    if 'best_cams' in locals():
        id_excluded_cams = id_cams_off_tot[best_cams]
    else:
        id_excluded_cams = list(range(n_cams))
        nb_cams_excluded = n_cams
    # print('id_excluded_cams ', id_excluded_cams)
    
    # If triangulation not successful, error = nan,  and 3D coordinates as missing values
    if error_min > error_threshold_triangulation:
        error_min = np.nan
        Q = np.array([np.nan, np.nan, np.nan])
        
    return Q, error_min, nb_cams_excluded, id_excluded_cams
                

def extract_files_frame_f(json_tracked_files_f, keypoints_ids):
    '''
    Extract data from json files for frame f, 
    in the order of the body model hierarchy.

    INPUTS:
    - json_tracked_files_f: list of str. Paths of json_files for frame f.
    - keypoints_ids: list of int. Keypoints IDs in the order of the hierarchy.

    OUTPUTS:
    - x_files, y_files, likelihood_files: array: 
      n_cams lists of n_keypoints lists of coordinates.
    '''

    n_cams = len(json_tracked_files_f)
    
    x_files, y_files, likelihood_files = [], [], []
    for cam_nb in range(n_cams):
        x_files_cam, y_files_cam, likelihood_files_cam = [], [], []
        with open(json_tracked_files_f[cam_nb], 'r') as json_f:
            js = json.load(json_f)
            for keypoint_id in keypoints_ids:
                try:
                    x_files_cam.append( js['people'][0]['pose_keypoints_2d'][keypoint_id*3] )
                    y_files_cam.append( js['people'][0]['pose_keypoints_2d'][keypoint_id*3+1] )
                    likelihood_files_cam.append( js['people'][0]['pose_keypoints_2d'][keypoint_id*3+2] )
                except:
                    x_files_cam.append( np.nan )
                    y_files_cam.append( np.nan )
                    likelihood_files_cam.append( np.nan )

        x_files.append(x_files_cam)
        y_files.append(y_files_cam)
        likelihood_files.append(likelihood_files_cam)
        
    x_files = np.array(x_files)
    y_files = np.array(y_files)
    likelihood_files = np.array(likelihood_files)

    return x_files, y_files, likelihood_files


def triangulate_all(config):
    '''
    For each frame
    For each keypoint
    - Triangulate keypoint
    - Reproject it on all cameras
    - Take off cameras until requirements are met
    Interpolate missing values
    Create trc file
    Print recap message
    
     INPUTS: 
    - a calibration file (.toml extension)
    - json files for each camera with only one person of interest
    - a Config.toml file
    - a skeleton model
    
    OUTPUTS: 
    - a .trc file with 3D coordinates in Y-up system coordinates 
    '''
    
    # Read config
    project_dir = config.get('project').get('project_dir')
    session_dir = os.path.realpath(os.path.join(project_dir, '..', '..'))
    pose_model = config.get('pose').get('pose_model')
    frame_range = config.get('project').get('frame_range')
    likelihood_threshold = config.get('triangulation').get('likelihood_threshold_triangulation')
    interpolation_kind = config.get('triangulation').get('interpolation')
    interp_gap_smaller_than = config.get('triangulation').get('interp_if_gap_smaller_than')
    show_interp_indices = config.get('triangulation').get('show_interp_indices')
    undistort_points = config.get('triangulation').get('undistort_points')

    calib_dir = [os.path.join(session_dir, c) for c in os.listdir(session_dir) if ('Calib' or 'calib') in c][0]
    calib_file = glob.glob(os.path.join(calib_dir, '*.toml'))[0] # lastly created calibration file
    pose_dir = os.path.join(project_dir, 'pose')
    poseTracked_dir = os.path.join(project_dir, 'pose-associated')
    
    # Projection matrix from toml calibration file
    P = computeP(calib_file, undistort=undistort_points)
    calib_params = retrieve_calib_params(calib_file)
        
    # Retrieve keypoints from model
    try: # from skeletons.py
        model = eval(pose_model)
    except:
        try: # from Config.toml
            model = DictImporter().import_(config.get('pose').get(pose_model))
            if model.id == 'None':
                model.id = None
        except:
            raise NameError('Model not found in skeletons.py nor in Config.toml')
    keypoints_ids = [node.id for _, _, node in RenderTree(model) if node.id!=None]
    keypoints_names = [node.name for _, _, node in RenderTree(model) if node.id!=None]
    keypoints_idx = list(range(len(keypoints_ids)))
    keypoints_nb = len(keypoints_ids)
    # for pre, _, node in RenderTree(model): 
    #     print(f'{pre}{node.name} id={node.id}')
    
    # left/right swapped keypoints
    keypoints_names_swapped = [keypoint_name.replace('R', 'L') if keypoint_name.startswith('R') else keypoint_name.replace('L', 'R') if keypoint_name.startswith('L') else keypoint_name for keypoint_name in keypoints_names]
    keypoints_names_swapped = [keypoint_name_swapped.replace('right', 'left') if keypoint_name_swapped.startswith('right') else keypoint_name_swapped.replace('left', 'right') if keypoint_name_swapped.startswith('left') else keypoint_name_swapped for keypoint_name_swapped in keypoints_names_swapped]
    keypoints_idx_swapped = [keypoints_names.index(keypoint_name_swapped) for keypoint_name_swapped in keypoints_names_swapped] # find index of new keypoint_name
    
    # 2d-pose files selection
    pose_listdirs_names = next(os.walk(pose_dir))[1]
    pose_listdirs_names = natural_sort(pose_listdirs_names)
    json_dirs_names = [k for k in pose_listdirs_names if 'json' in k]
    try: 
        json_files_names = [fnmatch.filter(os.listdir(os.path.join(poseTracked_dir, js_dir)), '*.json') for js_dir in json_dirs_names]
        json_files_names = [natural_sort(j) for j in json_files_names]
        json_tracked_files = [[os.path.join(poseTracked_dir, j_dir, j_file) for j_file in json_files_names[j]] for j, j_dir in enumerate(json_dirs_names)]
    except:
        json_files_names = [fnmatch.filter(os.listdir(os.path.join(pose_dir, js_dir)), '*.json') for js_dir in json_dirs_names]
        json_files_names = [natural_sort(j) for j in json_files_names]
        json_tracked_files = [[os.path.join(pose_dir, j_dir, j_file) for j_file in json_files_names[j]] for j, j_dir in enumerate(json_dirs_names)]
    
    # Triangulation
    f_range = [[0,min([len(j) for j in json_files_names])] if frame_range==[] else frame_range][0]
    frames_nb = f_range[1]-f_range[0]
    
    n_cams = len(json_dirs_names)
    Q_tot, error_tot, nb_cams_excluded_tot,id_excluded_cams_tot = [], [], [], []
    for f in tqdm(range(*f_range)):
        # Get x,y,likelihood values from files
        json_tracked_files_f = [json_tracked_files[c][f] for c in range(n_cams)]
        # print(json_tracked_files_f)
        x_files, y_files, likelihood_files = extract_files_frame_f(json_tracked_files_f, keypoints_ids)

        # undistort points
        if undistort_points:
            points = [np.array(tuple(zip(x_files[i],y_files[i]))).reshape(-1, 1, 2).astype('float32') for i in range(n_cams)]
            undistorted_points = [cv2.undistortPoints(points[i], calib_params['K'][i], calib_params['dist'][i], None, calib_params['optim_K'][i]) for i in range(n_cams)]
            x_files =  np.array([[u[i][0][0] for i in range(len(u))] for u in undistorted_points])
            y_files =  np.array([[u[i][0][1] for i in range(len(u))] for u in undistorted_points])
            # This is good for slight distortion. For fishey camera, the model does not work anymore. See there for an example https://github.com/lambdaloop/aniposelib/blob/d03b485c4e178d7cff076e9fe1ac36837db49158/aniposelib/cameras.py#L301

        # Replace likelihood by 0 if under likelihood_threshold
        with np.errstate(invalid='ignore'):
            x_files[likelihood_files<likelihood_threshold] = 0.
            y_files[likelihood_files<likelihood_threshold] = 0.
            likelihood_files[likelihood_files<likelihood_threshold] = 0.
        
        Q, error, nb_cams_excluded, id_excluded_cams = [], [], [], []
        for keypoint_idx in keypoints_idx:
        # Triangulate cameras with min reprojection error
            coords_2D_kpt = np.array( (x_files[:, keypoint_idx], y_files[:, keypoint_idx], likelihood_files[:, keypoint_idx]) )
            coords_2D_kpt_swapped = np.array(( x_files[:, keypoints_idx_swapped[keypoint_idx]], y_files[:, keypoints_idx_swapped[keypoint_idx]], likelihood_files[:, keypoints_idx_swapped[keypoint_idx]] ))

            Q_kpt, error_kpt, nb_cams_excluded_kpt, id_excluded_cams_kpt = triangulation_from_best_cameras(config, coords_2D_kpt, coords_2D_kpt_swapped, P, calib_params) # P has been modified if undistort_points=True

            Q.append(Q_kpt)
            error.append(error_kpt)
            nb_cams_excluded.append(nb_cams_excluded_kpt)
            id_excluded_cams.append(id_excluded_cams_kpt)
            
        # Add triangulated points, errors and excluded cameras to pandas dataframes
        Q_tot.append(np.concatenate(Q))
        error_tot.append(error)
        nb_cams_excluded_tot.append(nb_cams_excluded)
        id_excluded_cams = [item for sublist in id_excluded_cams for item in sublist]
        id_excluded_cams_tot.append(id_excluded_cams)
            
    Q_tot = pd.DataFrame(Q_tot)
    error_tot = pd.DataFrame(error_tot)
    nb_cams_excluded_tot = pd.DataFrame(nb_cams_excluded_tot)
    
    id_excluded_cams_tot = [item for sublist in id_excluded_cams_tot for item in sublist]
    cam_excluded_count = dict(Counter(id_excluded_cams_tot))
    cam_excluded_count.update((x, y/keypoints_nb/frames_nb) for x, y in cam_excluded_count.items())
    
    error_tot['mean'] = error_tot.mean(axis = 1)
    nb_cams_excluded_tot['mean'] = nb_cams_excluded_tot.mean(axis = 1)

    # Optionally, for each keypoint, show indices of frames that should be interpolated
    if show_interp_indices:
        zero_nan_frames = np.where( Q_tot.iloc[:,::3].T.eq(0) | ~np.isfinite(Q_tot.iloc[:,::3].T) )
        zero_nan_frames_per_kpt = [zero_nan_frames[1][np.where(zero_nan_frames[0]==k)[0]] for k in range(keypoints_nb)]
        gaps = [np.where(np.diff(zero_nan_frames_per_kpt[k]) > 1)[0] + 1 for k in range(keypoints_nb)]
        sequences = [np.split(zero_nan_frames_per_kpt[k], gaps[k]) for k in range(keypoints_nb)]
        interp_frames = [[f'{seq[0]}:{seq[-1]+1}' for seq in seq_kpt if len(seq)<=interp_gap_smaller_than and len(seq)>0] for seq_kpt in sequences]
        non_interp_frames = [[f'{seq[0]}:{seq[-1]+1}' for seq in seq_kpt if len(seq)>interp_gap_smaller_than] for seq_kpt in sequences]
    else:
        interp_frames = None
        non_interp_frames = []

    # Interpolate missing values
    if interpolation_kind != 'none':
        Q_tot = Q_tot.apply(interpolate_zeros_nans, axis=0, args = [interp_gap_smaller_than, interpolation_kind])
    # Q_tot.replace(np.nan, 0, inplace=True)
    
    # Create TRC file
    trc_path = make_trc(config, Q_tot, keypoints_names, f_range)
    
    # Recap message
    recap_triangulate(config, error_tot, nb_cams_excluded_tot, keypoints_names, cam_excluded_count, interp_frames, non_interp_frames, trc_path)
