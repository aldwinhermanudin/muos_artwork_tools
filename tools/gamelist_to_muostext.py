#!/usr/bin/env python3

import argparse
import os
from lxml import etree

TEXT_EXTENSION = 'txt'

# Run the main function when the script is executed directly
if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Convert Emulation Station gamelist.xml to MuOS Text")
    parser.add_argument('--input-file', type=argparse.FileType('r'), help="Path to the XML file", required=True)
    parser.add_argument('--output-directory', type=str, help="Path to the output text directory", required=True)

    # Parse arguments
    args = vars(parser.parse_args())

    input_file = args["input_file"]
    output_directory = args["output_directory"].rstrip('/')

    if not os.path.isdir(output_directory):
        print("Output directory not exist!")
        exit(1)

    # Parse XML file
    tree = etree.parse(input_file)  # Replace with your XML file path
    root = tree.getroot()

    # Access elements
    for game in root.findall('game'):
        try:
            basename = os.path.splitext(os.path.basename( game.find('path').text ))[0]
            desc = game.find('desc').text        
            
            if type(basename) is str and type(desc) is str:
                # Write variable data to the file
                with open(output_directory + "/" + basename + "." + TEXT_EXTENSION, 'w') as file:
                    file.write(desc)
        except Exception as e:
            continue

        