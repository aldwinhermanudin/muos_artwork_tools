#!/usr/bin/env python3

from PIL import Image
import argparse
import os


# Run the main function when the script is executed directly
if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Convert Pico-8 Game as Artwork")
    parser.add_argument('--input-directory', type=str, help="Path to the input pico-8 directory", required=True)
    parser.add_argument('--output-directory', type=str, help="Path to the output text directory", required=True)

    # Parse arguments
    args = vars(parser.parse_args())

    input_directory = args["input_directory"].rstrip('/')
    output_directory = args["output_directory"].rstrip('/')

    for root, dirs, files in os.walk(input_directory):
        for file in files:

            filepath = os.path.join(root, file)
            basename = os.path.basename( filepath )
            print(filepath)

            if filepath.lower().endswith(".png"):
                # Load the image you want to center
                image = Image.open(os.path.join(root, file))
                
                # Set the scaling factor or new size
                scaling_factor = 1.5  # For example, to double the image size
                new_width = int(image.width * scaling_factor)
                new_height = int(image.height * scaling_factor)

                # Upscale the image using a high-quality resampling filter
                # upscaled_image = image.resize((new_width, new_height), Image.NEAREST)
                upscaled_image = image.resize((new_width, new_height), Image.LANCZOS)

                # Define the size of the larger canvas
                canvas_width = 320  # Replace with your desired width
                canvas_height = 420  # Replace with your desired height

                # Create a new blank canvas with a white background (you can choose any color)
                canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

                # Calculate the top-left position to paste the image, so it's centered
                x = (canvas_width - upscaled_image.width) // 2
                y = (canvas_height - upscaled_image.height) // 2

                # Paste the image onto the canvas
                canvas.paste(upscaled_image, (x, y))

                # Save or show the final image
                # canvas.save( output_directory + "/" + basename, "PNG", optimize=True, quality=85)  # To save the image
                canvas.save( output_directory + "/" + basename)  # To save the image

