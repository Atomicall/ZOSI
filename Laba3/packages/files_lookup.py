import os
import os.path
import re

def find_files_by_regex(lookup_folder: str, reg_exp: str) -> list:
    images = []
    if os.path.exists(lookup_folder):
        for dirpath, dirnames , files in os.walk(os.path.join(".", lookup_folder)):
            for file in files:
                if re.match(reg_exp, file):
                    images.append(os.path.join(dirpath,file))
    return images