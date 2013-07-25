#! /usr/bin/env python

"""
This is a Python script to run automatic tests on Plastimatch mabs (www.plastimatch.org)
"""

import os
import subprocess

parameters={}

####################################
### Parameters setting - BEGIN - ###
####################################

parameters["enable_atlas_selection"]=[]
parameters["atlas_selection_criteria"]=[]
parameters["roi_mask"]=[]
parameters["mi_percent_thershold"]=[]
parameters["mi_histogram_bins"]=[]
parameters["lower_mi_value"]=[]
parameters["upper_mi_value"]=[]

parameters["atlas_dir"]=[]
parameters["training_dir"]=[]

parameters["rho_values"]=[]
parameters["sigma_values"]=[]
parameters["minimum_similarity"]=[]
parameters["threshold_values"]=[]

parameters["write_thresholded_files"]=[]
parameters["write_weight_files"]=[]
parameters["write_distance_map"]=[]
parameters["compute_distance_map"]=[]

####################################
###  Parameters setting - END -  ###
####################################

####################################
###   Paths setting  - BEGIN -   ###
####################################

# SET FULL PATHS
plastimatch_path="" # if empty will be used the default installed plastimatch
config_files_folder="config_files"

####################################
###    Paths setting  - END -    ###
####################################

# Adjust paths
plastimatch_path.rstrip("\\/")
config_files_folder.rstrip("\\/")

# Find the non fixed parameters
non_fixed_parms=[]
for parameter in parameters:
    if type(parameters[parameter]) is tuple or type(parameters[parameter]) is list:
        non_fixed_parms.append(parameter)

# Compute all possible combinations
combinations=[[]]

for parm in non_fixed_parms:
    parm=parameters[parm]
    temp = []
    for x in parm:
        for i in combinations:
            temp.append(i+[x])
    combinations = temp

# Write parms files
os.makedirs(config_files_folder)

for i, combination in enumerate(combinations):
    fid = open(config_files_folder + os.sep + "mabs_test_" + str(i) + ".cfg", "w")

    for parameter in parameters:
        if not parameter in non_fixed_parms:
            fid.write(parameter + " = " + str(parameters[parameter]) +"\n")
        elif parameter in non_fixed_parms:
            index = non_fixed_parms.index(parameter)
            fid.write(parameter + " = " + str(combination[index]) +"\n")
    
    fid.close()

# Run plastimatch mabs
if plastimatch_path == "":
    plastimatch_executable = "plastimatch"
elif plastimatch_path != "":
    plastimatch_executable = plastimatch_path + os.sep + "plastimatch"

for cfg_file in os.listdir(config_files_folder):
    if cfg_files.endswith(".cfg"):
        subprocess.call(plastimatch_executable + " mabs --train-registration " + config_files_folder + os.sep + cfg_files)
        subprocess.call(plastimatch_executable + " mabs --train " + config_files_folder + os.sep + cfg_files)
    elif not cfg_files.endswith(".cfg"):
        print(config_files_folder + os.sep + cfg_file + " ignored \n")
