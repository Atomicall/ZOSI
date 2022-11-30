import os.path as path
import skimage.io

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def generate_images_from_letters(letters_list: list, out_path: str,  font_path: str, font_size: int, img_format: str):
    if path.exists(font_path):
        print(f"[INFO] Generating images from {letters_list} letters...")
        print(f"\tUsing {font_path}")
        font = ImageFont.truetype(font_path, font_size)
        size = (max([ font.getsize(l)[0] for l in letters_list]), max([ font.getsize(l)[1] for l in letters_list]))
        images_list = [ Image.new('1', size, 1) for _ in letters_list]
        for image, letter in zip(images_list, letters_list):
            image_path = path.join(out_path, f"{letter}.{img_format}")
            ImageDraw.Draw(image).text((0,0), letter, font=font)
            image.save(image_path)
            print(f"\tSaved {letter} as {image_path}")
    else: 
        raise Exception(f"[ERROR] Unable to find font {font_path}")
    
        