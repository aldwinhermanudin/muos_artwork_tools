#!/usr/bin/env python3

from PIL import Image, ImageOps
import argparse
import os
import math
def resize_image(input_path, output_path, target_size=(320, 420), outer_border=10):

    smallest_size = target_size[0] if target_size[0] < target_size[1] else target_size[1]
    smallest_size = smallest_size - (outer_border*2)

    # Open the original image
    with Image.open(input_path) as img:
        # Calculate the aspect ratio
        img = ImageOps.fit(img, (smallest_size,smallest_size), method=Image.LANCZOS)

        # Create a new image with a white background
        # new_image = Image.new("RGB", target_size, (255, 255, 255))
        new_image = Image.new("RGBA", target_size, (0, 0, 0, 0))

        # Calculate positioning for centering
        x_offset = (target_size[0] - img.width) // 2
        y_offset = (target_size[1] - img.height) // 2

        # shift down a bit
        y_offset = y_offset + 20

        # Paste the resized image onto the new image
        new_image.paste(img, (x_offset, y_offset))

        # Save the new image
        new_image.save(output_path)

# Run the main function when the script is executed directly
if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Convert Pico-8 Game as Artwork")
    parser.add_argument('--input-directory', type=str, help="Path to the input pico-8 directory", required=True)
    parser.add_argument('--output-directory', type=str, help="Path to the output directory", required=True)
    parser.add_argument('--width', type=int, help="Final image width", required=True)
    parser.add_argument('--height', type=int, help="Final image height", required=True)
    parser.add_argument('--outer-border', type=int, help="Outer Border", required=True)

    # Parse arguments
    args = vars(parser.parse_args())

    input_directory = args["input_directory"].rstrip('/')
    output_directory = args["output_directory"].rstrip('/')
    width = args["width"]
    height = args["height"]
    outer_border = args["outer_border"]

    # list all images
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            filepath = os.path.join(root, file)
            # print(filepath)
            try:
               resize_image(filepath, output_directory + "/" + os.path.basename(file), outer_border=outer_border)
            except Exception as e:
                print("error occurs: {}".format(e))