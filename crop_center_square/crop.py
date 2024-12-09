import os
import sys
from PIL import Image, UnidentifiedImageError

def center_crop_to_square(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            side = min(width, height)
            left = (width - side) // 2
            top = (height - side) // 2
            right = left + side
            bottom = top + side
            cropped_img = img.crop((left, top, right, bottom))
            save_cropped_image(image_path, cropped_img)
    except UnidentifiedImageError:
        print(f"Unsupported or invalid image format: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def custom_crop(image_path, width, height, position):
    try:
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            
            positions = {
                "top-left": (0, 0),
                "center-left": (0, (img_height - height) // 2),
                "bottom-left": (0, img_height - height),
                "top-center": ((img_width - width) // 2, 0),
                "center-center": ((img_width - width) // 2, (img_height - height) // 2),
                "bottom-center": ((img_width - width) // 2, img_height - height),
                "top-right": (img_width - width, 0),
                "center-right": (img_width - width, (img_height - height) // 2),
                "bottom-right": (img_width - width, img_height - height),
            }

            if position not in positions:
                raise ValueError(f"Invalid position: {position}")

            left, top = positions[position]
            right = left + width
            bottom = top + height

            if right > img_width or bottom > img_height:
                raise ValueError("Crop dimensions exceed image bounds")

            cropped_img = img.crop((left, top, right, bottom))
            save_cropped_image(image_path, cropped_img)
    except UnidentifiedImageError:
        print(f"Unsupported or invalid image format: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def save_cropped_image(image_path, cropped_img):
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    cropped_path = os.path.join(directory, f"{name}-cropped{ext}")
    cropped_img.save(cropped_path, format=cropped_img.format)
    print(f"Cropped and saved as: {cropped_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python image_crop.py <image_path> [--custom width height position]")
        return

    image_path = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--custom":
        if len(sys.argv) != 6:
            print("Usage for custom crop: python image_crop.py <image_path> --custom <width> <height> <position>")
            return
        try:
            width = int(sys.argv[3])
            height = int(sys.argv[4])
            position = sys.argv[5]
            custom_crop(image_path, width, height, position)
        except ValueError as e:
            print(f"Invalid input: {e}")
    else:
        center_crop_to_square(image_path)

if __name__ == "__main__":
    main()
