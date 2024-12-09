import os
import sys
from PIL import Image, UnidentifiedImageError

def center_crop_to_square(image_path):
    try:
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
            # Crop the image
            cropped_img = img.crop((left, top, right, bottom))
            # Generate new file name
            directory, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)
            cropped_path = os.path.join(directory, f"{name}-cropped{ext}")
            # Save the cropped image, preserving format
            cropped_img.save(cropped_path, format=img.format)
            print(f"Cropped and saved as: {cropped_path}")
    except UnidentifiedImageError:
        print(f"Unsupported or invalid image format: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main(file_paths):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            center_crop_to_square(file_path)
        else:
            print(f"Skipping non-file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Processing files... Drag and drop multiple files to batch process.")
        main(sys.argv[1:])
    else:
        print("No images provided. Drag and drop files onto the batch script.")
