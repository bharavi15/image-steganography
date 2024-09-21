# from typing import Str
from cv2 import imread, imwrite
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
log = logging.getLogger()

def convert_file_to_png(file_name: str):
    file_base_name = file_name.split('.')[0]
    if file_name.endswith(('.jpg','.jpeg')):
        imwrite(f"{file_base_name}.png", imread(file_name))
    elif file_name.endswith('png'):
        imwrite(f"{file_name}.png", imread(file_name))
    else:
        log.error('File extension is not jpg or jpeg')

def read_image(file_name):
    return imread(file_name)

def steg_a_pixel(pixel:tuple[int,int,int],steg_data:str):
    pass
if __name__ == '__main__':
    convert_file_to_png('DSCN0982.png')