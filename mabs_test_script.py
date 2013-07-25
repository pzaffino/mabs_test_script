#! /usr/bin/env python

"""
This is a Python script to run automatic tests on Plastimatch mabs (www.plastimatch.org)
"""

import os
import subprocess

parameters={}

################################################################ SECTION EDITABLE BY USER - BEGIN - ####################################################

####################################
### Parameters setting - BEGIN - ###
####################################

# [PREALIGNMENT]
parameters["reference"]=[]
parameters["registration_config"]=[]
parameters["spacing"]=[]

# [ATLASES-SELECTION]
parameters["enable_atlas_selection"]=[]
parameters["atlas_selection_criteria"]=[]
parameters["roi_mask"]=[]
parameters["mi_percent_thershold"]=[]
parameters["mi_histogram_bins"]=[]
parameters["lower_mi_value"]=[]
parameters["upper_mi_value"]=[]

# [TRAINING]
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

# [REGISTRATION]
parameters["registration_config"]=[]

# [LABELING]
parameters["input"]=[]
parameters["output"]=[]

# [STRUCTURES]
parameters["structures"]=[]
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

################################################################# SECTION EDITABLE BY USER - END - #####################################################

# Assign parameters to them section
sections = ("atlas-selection", "prealignment", "training", "registration", "labeling", "structures")

prealignment_parms = ("reference", "registration_config", "spacing")
atlases_selection_parms = ("enable_atlas_selection", "atlas_selection_criteria", "roi_mask",
                           "mi_percent_thershold", "mi_histogram_bins", "lower_mi_value", "upper_mi_value")
training_parms = ("atlas_dir", "training_dir", "rho_values", "sigma_values", "minimum_similarity", "threshold_values",
                  "write_thresholded_files", "write_weight_files", "write_distance_map", "compute_distance_map")
registration_parms = ("registration_config")
labeling_parms = ("input", "output")

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

    for section in sections[:-1]: # No section "structures"
        fid.write("[" + section.upper()  + "] \n"
        
        for parameter in parameters:
            if parameter in vars()[section.replace("_", "-") + "_parms"]:
                if parameters[parameter] and not parameter in non_fixed_parms:
                    fid.write(parameter + " = " + str(parameters[parameter]) +"\n")
                elif parameters[parameter] and parameter in non_fixed_parms:
                    index = non_fixed_parms.index(parameter)
                    fid.write(parameter + " = " + str(combination[index]) +"\n")
        
    fid.write("[STRUCTURES] \n")
    for structure in parameters["structures"]:
        fid.write(structure)
    
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
