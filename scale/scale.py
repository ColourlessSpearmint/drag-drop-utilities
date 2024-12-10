import os
import sys
from PIL import Image, UnidentifiedImageError


def scale_image(image_path, scale_factor):
    try:
        with Image.open(image_path) as img:
            # Calculate new dimensions
            width, height = img.size
            new_width = int(width * (scale_factor / 100))
            new_height = int(height * (scale_factor / 100))

            # Resize image using LANCZOS filter for high-quality resizing
            scaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the scaled image with the new name
            save_scaled_image(image_path, scaled_img)
    except UnidentifiedImageError:
        print(f"Unsupported or invalid image format: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def save_scaled_image(image_path, scaled_img):
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    scaled_path = os.path.join(directory, f"{name}-scaled{ext}")
    scaled_img.save(scaled_path, format=scaled_img.format)
    print(f"Scaled and saved as: {scaled_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python image_scale.py <image_path(s)>")
        return

    # Ask user for the scale factor percentage
    try:
        scale_factor = float(
            input("Enter the scale factor as a percentage (e.g., 50 for 50%): ")
        )
        if scale_factor <= 0:
            print("Scale factor must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Process each image
    for image_path in sys.argv[1:]:
        if os.path.isfile(image_path):
            scale_image(image_path, scale_factor)
        else:
            print(f"Skipping non-file: {image_path}")


if __name__ == "__main__":
    main()
