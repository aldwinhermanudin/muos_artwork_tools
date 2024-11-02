#!/usr/bin/env python3

from PIL import Image, ImageOps
import argparse
import os
import shutil
from pathlib import Path
import json

KNOWN_PARENT_WAD = [
    'doom2.wad',
    'DOOM.WAD', 
    'DOOM2.WAD', 
    'freedoom1.wad', 
    'doom.wad',
    'freedoom2.wad'
]

PRBOOM_CFG_FILE = "prboom.cfg"

def list_files_in_dir( dir_path: str):
    res_files = []
    # Iterate over all files in the root of the directory
    for entry in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry)
        if os.path.isfile(full_path):  # Check if it's a file
            res_files.append(full_path)

    return res_files

def recursive_list_files_in_dir( dir_path: str):
    res_files = []
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            filepath = os.path.join(root, file)
            res_files.append(filepath)

    return res_files

def list_potential_pwad( dir_path:str):
    
    all_files = recursive_list_files_in_dir(dir_path)
    pwad_list = {}
    for afile in all_files:
        filename = os.path.basename(afile)
        if "doom" in filename.lower() and ".wad" in filename.lower():
            if not filename in pwad_list:
                pwad_list[filename] = {}
                pwad_list[filename]["count"] = 1
                pwad_list[filename]["path"] = afile
            else:
                pwad_list[filename]["count"] = pwad_list[filename]["count"] + 1

    print(json.dumps(pwad_list, indent=4))
    
    # Get a list of keys and print them
    return list(pwad_list.keys())


# Run the main function when the script is executed directly
if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Convert Pico-8 Game as Artwork")
    parser.add_argument('--input-directory', type=str, help="Path to the input RG35XX Doom rom directory", required=True)
    parser.add_argument('--output-directory', type=str, help="Path to the output directory", required=True)

    # Parse arguments
    args = vars(parser.parse_args())

    input_directory = args["input_directory"].rstrip('/')
    output_directory = args["output_directory"].rstrip('/')
    
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".sh"):
                filepath = os.path.join(root, file)
                filename = os.path.basename(filepath)
                filename_without_extension = os.path.splitext(os.path.basename(filepath))[0]
                print( filepath )

                # Open the file and search for the line
                with open(filepath, "r") as file:
                    for line in file:
                        # Check if the specific text is in the line
                        if "/mnt/mmc/CFW/retroarch/.retroarch/cores/prboom_libretro.so" in line:
                            # Find all parts enclosed in double quotes
                            parts_in_quotes = line.split('"')
                            
                            # Check if there's at least one quoted part after the specific text
                            if len(parts_in_quotes) > 2:
                                # The last quoted part is near the end of the line
                                wad_path = parts_in_quotes[-2]
                                wad_path = wad_path.replace("$progdir", input_directory)
                                wad_filename = os.path.basename(wad_path)
                                wad_filename_without_extension = os.path.splitext(os.path.basename(wad_filename))[0]

                                # get wad directory path
                                wad_dir_path = os.path.dirname(wad_path)
                                print("wad path:", wad_path)
                                print("wad dir path:", wad_dir_path)

                                # check if this wad has it's own directory
                                # if a dir has more than ~ 50 files, then it's has multiple wad
                                is_own_dir = True if len(recursive_list_files_in_dir(wad_dir_path)) < 50  else False
                                print("wad has it's own dir: ", is_own_dir)

                                # create directory for that wad
                                doom_output_dir = os.path.join(output_directory, "." + filename_without_extension)
                                if not os.path.exists(doom_output_dir):
                                    os.makedirs(doom_output_dir)

                                all_files = list_files_in_dir(wad_dir_path)

                                # check if wad has it's own dir
                                if is_own_dir:
                                    # copy all files to new directory
                                    for filec in all_files:
                                        # generate dest file
                                        filec_name = os.path.basename(filec)
                                        filec_dest_path = os.path.join(doom_output_dir, filec_name)

                                        # copy file
                                        shutil.copy(filec, filec_dest_path)

                                        print("copy {} to {}".format(filec_name, filec_dest_path ))
                                else:
                                    # copy all file that has the wad name in the filename
                                    # hopefully this will copy the wad and the related txt file
                                    for afile in all_files:
                                        afile_basename = str(os.path.basename(afile))
                                        if wad_filename_without_extension.lower() in afile_basename.lower():
                                            shutil.copy(afile, os.path.join(doom_output_dir, afile_basename))
                                            print("copy {} to {}".format(afile, os.path.join(doom_output_dir, afile_basename) ))

                                    # also copy the pwad file
                                    pwad_file = ""
                                    for k_wad in KNOWN_PARENT_WAD:
                                        for afile in all_files:
                                            if k_wad.lower() in afile.lower():
                                                pwad_file = afile

                                                afile_basename = str(os.path.basename(afile))
                                                shutil.copy(afile, os.path.join(doom_output_dir, afile_basename))
                                                print("copy {} to {}".format(afile, os.path.join(doom_output_dir, afile_basename) ))
                                                break
                                            
                                        if len(pwad_file) != 0:
                                            break


                                # check if wad has pr_boom.cfg
                                has_pr_boom_cfg = False
                                for afile in all_files:
                                    has_pr_boom_cfg = True if PRBOOM_CFG_FILE in afile else False
                                print("wad has pr_boom.cfg? ", has_pr_boom_cfg)


                                # Create the .doom file
                                doom_output_file = os.path.join(output_directory, filename_without_extension + ".doom")
                                if has_pr_boom_cfg:
                                    # look for pr_boom.cfg
                                    matching_files = [file for file in all_files if PRBOOM_CFG_FILE in file]
                                    # hopefully only 1 matched file
                                    pr_boom_cfg_file = matching_files[0]

                                    # modify wadfile_1 to parentwad and shift wadfile_<x> to wadfile_<x-1>
                                    print("config copy & update {} to {}".format(pr_boom_cfg_file, doom_output_file ))
                                    with open(pr_boom_cfg_file, 'r') as cfg_file, open(doom_output_file, 'w') as doom_file :
                                        wadfile_counter = 0
                                        has_pwad_as_wadfile_1 = False
                                        for line in cfg_file:

                                            # check if cfg has pwad as wadfile_1
                                            if "wadfile_1" in line:
                                                for k_pwad in KNOWN_PARENT_WAD:
                                                    if k_pwad in line:
                                                        line = line.replace("wadfile_1", "parentwad" )
                                                        has_pwad_as_wadfile_1 = True
                                                        wadfile_counter = 1

                                            # shift wadfile_ by 1
                                            if has_pwad_as_wadfile_1 and "wadfile_" in line:
                                                line = line.replace( "wadfile_"+ str(wadfile_counter+1), "wadfile_"+ str(wadfile_counter) )
                                                wadfile_counter = wadfile_counter + 1


                                            # write to new file
                                            doom_file.write(line)
                                else:
                                    # check if wad has a known wad
                                    pwad_file = ""
                                    for k_wad in KNOWN_PARENT_WAD:
                                        for afile in all_files:
                                            if k_wad.lower() in afile.lower():
                                                pwad_file = afile
                                                print("found pwad file: ", pwad_file)
                                                break
                                        if len(pwad_file) != 0:
                                            break
                                    has_pwad = (len(pwad_file) > 0)
                                    
                                    print("has pwad: ", has_pwad)

                                    # Open the file in write mode
                                    with open(doom_output_file, 'w') as doom_file:
                                        if has_pwad:                                    
                                            pwad_filename = str(os.path.basename(pwad_file))
                                            pwad_line = "parentwad " + "\"" + pwad_filename + "\"" + "\n"
                                            doom_file.write(pwad_line)
                                        
                                            wad_line = "wadfile_1 " + "\"" + wad_filename + "\""
                                            doom_file.write(wad_line)
                                        else:
                                            wad_line = "parentwad " + "\"" + wad_filename + "\""
                                            doom_file.write(wad_line)