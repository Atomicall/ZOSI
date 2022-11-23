import os
import os.path

def find_images(lookup_folder: str) -> list:
    images = []
    if os.path.exists(lookup_folder):
        for dirpath, dirnames , files in os.walk(os.path.join(".", lookup_folder)):
            for file in files:
                if file.split(".")[-1] in ["jpg", "png"]:
                    images.append(os.path.join(dirpath,file))
    return images