import os
from PIL import Image


def process_images_in_folder(folder_path):
    image_files = [
        f for f in os.listdir(folder_path) if f.lower().endswith((".jpeg", ".jpg"))
    ]

    i = 1
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)

        # Open the image
        with Image.open(img_path) as img:
            # Convert to RGB (in case it's a HEIC file)
            img = img.convert("RGB")
            img_cropped = crop_image_to_aspect_ratio(img, 3, 4)

            # Resize to 800px width while maintaining aspect ratio
            base_width = 800
            width_percent = base_width / float(img_cropped.width)
            new_height = int(width_percent * float(img_cropped.height))
            img_resized = img_cropped.resize((base_width, new_height), Image.LANCZOS)

            img_resized.save(img_path, "JPEG", quality=95)


def crop_image_to_aspect_ratio(img, target_width, target_height):
    """
    Crop the provided image to the target aspect ratio.
    """
    img_width, img_height = img.size

    # Calculate target aspect ratio
    target_ratio = target_width / target_height
    img_ratio = img_width / img_height

    # Depending on the current aspect ratio of the image, we'll need to crop differently
    if img_ratio > target_ratio:
        # Current image is too wide, adjust the width
        new_width = int(target_ratio * img_height)
        left = (img_width - new_width) / 2
        top = 0
        right = (img_width + new_width) / 2
        bottom = img_height
    else:
        # Current image is too tall, adjust the height
        new_height = int(img_width / target_ratio)
        left = 0
        top = (img_height - new_height) / 2
        right = img_width
        bottom = (img_height + new_height) / 2

    return img.crop((left, top, right, bottom))


if __name__ == "__main__":
    process_images_in_folder("/Users/pietz/Downloads/bluff3")
