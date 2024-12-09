import os
import sys
from PIL import Image

def center_crop_to_square(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Get dimensions
        width, height = img.size
        # Calculate the size of the square
        side = min(width, height)
        # Calculate cropping box
        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side
        # Crop and save the image
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(image_path)  # Overwrite the original file

def main(file_paths):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            try:
                center_crop_to_square(file_path)
                print(f"Cropped: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        else:
            print(f"Skipping non-file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print("No images provided. Drag and drop files onto the batch script.")