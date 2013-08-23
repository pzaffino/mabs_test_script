#! /usr/bin/env python

"""
This is a Python script to run automatic tests on Plastimatch mabs (www.plastimatch.org)
Author: Paolo Zaffino (p dot zaffino at unicz dot it)
Tested on Python 2.7 and on Python 3.3
"""

import os
import shutil
import subprocess

prealignment={}
atlas_selection={}
training={}
registration={}
labeling={}
structures={}
parameters={}
parameters["prealignment"]=prealignment
parameters["atlas-selection"]=atlas_selection
parameters["training"]=training
parameters["registration"]=registration
parameters["labeling"]=labeling
parameters["structures"]=structures

################################################################ SECTION EDITABLE BY USER - BEGIN - ####################################################

# HOW SET THE PARAMETERS:
# - Do not remove an unused dictionary entry, set it as a empty list
# - If you want to set just a value for a parameter set it as a list having just an element
# - If you want to set more than one value for a parameter set them inside a list

####################################
### Parameters setting - BEGIN - ###
####################################

# [PREALIGNMENT]
parameters["prealignment"]["reference"]=[]
parameters["prealignment"]["registration_config"]=[]
parameters["prealignment"]["spacing"]=[]

# [ATLASES-SELECTION]
parameters["atlas-selection"]["enable_atlas_selection"]=["true"]
parameters["atlas-selection"]["atlas_selection_criteria"]=["random"]
parameters["atlas-selection"]["nmi_ratio_registration_config"]=[]
parameters["atlas-selection"]["roi_mask"]=[]
parameters["atlas-selection"]["mi_percent_thershold"]=[]
parameters["atlas-selection"]["mi_histogram_bins"]=[]
parameters["atlas-selection"]["lower_mi_value"]=[]
parameters["atlas-selection"]["upper_mi_value"]=[]
parameters["atlas-selection"]["min_random_atlases"]=[]
parameters["atlas-selection"]["max_random_atlases"]=[]

# [TRAINING]
parameters["training"]["atlas_dir"]=["atlas-mgh"]
parameters["training"]["training_dir"]=["training-mgh"]
parameters["training"]["rho_values"]=[0.5, 0.6]
parameters["training"]["sigma_values"]=[1.5, 2.0]
parameters["training"]["minimum_similarity"]=[0.25]
parameters["training"]["threshold_values"]=[0.2,0.3,0.4,0.5]
parameters["training"]["write_thresholded_files"]=[1]
parameters["training"]["write_weight_files"]=[1]
parameters["training"]["write_distance_map"]=[]
parameters["training"]["compute_distance_map"]=[]

# [REGISTRATION]
parameters["registration"]["registration_config"]=["mgh-parms.txt"]

# [LABELING]
parameters["labeling"]["input"]=[]
parameters["labeling"]["output"]=[]

# [STRUCTURES]
parameters["structures"]["structures"]=["left_parotid", "left_parotid_corr"]
####################################
###  Parameters setting - END -  ###
####################################

####################################
###   Paths setting  - BEGIN -   ###
####################################

# HOW SET THE PATHS:
# - Use full paths
# - If "plastimatch_path" is unsetted (empty string) will be used the default path for plastimatch executable (that installed into the system path)

plastimatch_path=""
config_files_folder="/home/USER/mabs/config_files"

####################################
###    Paths setting  - END -    ###
####################################

################################################################# SECTION EDITABLE BY USER - END - #####################################################

print("START! \n")

# Assign parameters to them section
sections = ("prealignment", "atlas-selection", "training", "registration", "labeling", "structures")

# Adjust paths
plastimatch_path = plastimatch_path.rstrip("\\/")
config_files_folder = config_files_folder.rstrip("\\/")

# Find the non fixed parameters
non_fixed_parms=[]
for section in parameters:
    for parameter in parameters[section]:
        if len(parameters[section][parameter]) > 1:
            non_fixed_parms.append([section, parameter, parameters[section][parameter]])

# Compute all possible combinations
combinations=[[]]

print("Computing all the possible parameters combinations \n")

for parm in non_fixed_parms:
    parm=parm[2]
    temp = []
    for x in parm:
        for i in combinations:
            temp.append(i+[x])
    combinations = temp

print("All the possible parameters combinations are " + str (len(combinations)) + "\n")

# Write parms files
print("Writing configuration files \n")

if os.path.exists(config_files_folder):
   shutil.rmtree(config_files_folder)

os.mkdir(config_files_folder)

for i, combination in enumerate(combinations):
    fid = open(config_files_folder + os.sep + "mabs_test_" + str(i+1) + ".cfg", "w")

    for section in sections[:-1]: # No section "structures"
        non_fixed_stage_parms = [p[1] for p in non_fixed_parms if p[0] == section]
        
        section_empty=True

        for parameter in parameters[section]:
            if parameters[section][parameter]:
                section_empty=False
                break

        if not section_empty:
            fid.write("[" + section.upper()  + "] \n")
        
            for parameter in parameters[section]:
                if parameters[section][parameter] and not parameter in non_fixed_stage_parms:
                    assert len(parameters[section][parameter]) == 1
                    fid.write(parameter + " = " + str(parameters[section][parameter][0]) +"\n")
                elif parameters[section][parameter] and parameter in non_fixed_stage_parms:
                     index = non_fixed_stage_parms.index(parameter)
                     fid.write(parameter + " = " + str(combination[index]) +"\n")
            fid.write("\n")
    
    fid.write("[STRUCTURES] \n")
    for structure in parameters["structures"]["structures"]:
        fid.write(structure + "\n")
    
    fid.close()

# Run plastimatch mabs
if plastimatch_path == "":
    plastimatch_executable = "plastimatch"
elif plastimatch_path != "":
    plastimatch_executable = plastimatch_path + os.sep + "plastimatch"

for cfg_file in os.listdir(config_files_folder):
    if cfg_file.endswith(".cfg"):
        print("Running plastimatch mabs using the file " + cfg_file  + "\n")
        command = plastimatch_executable + " mabs --train-registration "
        conf_file = config_files_folder + os.sep + cfg_file
        c = command + conf_file
        subprocess.call(plastimatch_executable + " mabs --train-registration " + config_files_folder + os.sep + cfg_file, shell=True)
        subprocess.call(plastimatch_executable + " mabs --train " + config_files_folder + os.sep + cfg_file, shell=True)
    elif not cfg_file.endswith(".cfg"):
        print(config_files_folder + os.sep + cfg_file + " ignored \n")

print("FINISHED! \n")

