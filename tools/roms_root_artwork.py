#!/usr/bin/env python3

from PIL import Image, ImageOps
import argparse
import os
import math

def combine_images(images, canvas_size=(320, 420), cols=2, border_size=5, outer_border=10):
    # Create a blank canvas
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    
    # Calculate available width and height (with space for borders)
    num_images = len(images)
    grid_cols = cols  # for a 2-column layout (adjust if needed)
    grid_rows = (num_images + 1) // grid_cols  # calculate rows needed
    
    # Determine max size for each image to fit within canvas with borders
    max_width = (canvas_size[0] - (grid_cols + 1) * border_size) // grid_cols
    max_height = (canvas_size[1] - (grid_rows + 1) * border_size) // grid_rows
    
    smallest_size = max_width if max_width < max_height else max_height
    
    print(smallest_size)
    # Resize and place each image
    for i, img in enumerate(images):
        # Open image
        img = Image.open(img)

        # Resize while keeping aspect ratio
        img = ImageOps.fit(img, (smallest_size, smallest_size), method=Image.LANCZOS)
        # img.thumbnail((smallest_size,smallest_size), Image.LANCZOS)
        
        # Calculate position on the canvas
        x = (i % grid_cols) * (max_width + border_size) + border_size
        y = (i // grid_cols) * (max_height + border_size) + border_size
        
        # Paste the image on the canvas
        canvas.paste(img, (x, y))
    
    resize_value = ( canvas_size[0] - (outer_border*2), canvas_size[1] - (outer_border*2),   )
    resized_img = canvas.resize((resize_value[0], resize_value[1]), Image.LANCZOS)

    x = (canvas_size[0] - resize_value[0]) // 2
    y = (canvas_size[1] - resize_value[1]) // 2

    # shift down a bit
    y = 20

    # create final canvas, and copy the resize image to the middle
    # final_canvas = Image.new("RGB", canvas_size, (255, 255, 255))
    final_canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    final_canvas.paste(resized_img, (x, y) )

    return final_canvas

# Run the main function when the script is executed directly
if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Convert Pico-8 Game as Artwork")
    parser.add_argument('--input-directory', type=str, help="Path to the input pico-8 directory", required=True)
    parser.add_argument('--output-file', type=str, help="Path to the output file", required=True)
    parser.add_argument('--width', type=int, help="Final image width", required=True)
    parser.add_argument('--height', type=int, help="Final image height", required=True)
    parser.add_argument('--column', type=int, help="Column", required=True)
    parser.add_argument('--inner-border', type=int, help="Inner Border", required=True)
    parser.add_argument('--outer-border', type=int, help="Outer Border", required=True)

    # Parse arguments
    args = vars(parser.parse_args())

    input_directory = args["input_directory"].rstrip('/')
    output_file = args["output_file"]
    width = args["width"]
    height = args["height"]
    column = args["column"]
    inner_border = args["inner_border"]
    outer_border = args["outer_border"]

    
    # Example usage
    image_paths = []

    # list all images
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            filepath = os.path.join(root, file)

            # add filepath to image paths
            image_paths.append(filepath)

    grid_img = combine_images( image_paths, canvas_size=(width, height), cols=column, border_size=inner_border, outer_border=outer_border)
    grid_img.save(output_file)  # Save the final grid image