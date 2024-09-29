# from typing import Str
from cv2 import imread, imwrite
import logging
import numpy as np

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger()


def convert_file_to_png(file_name: str):
    file_base_name = file_name.split(".")[0]
    if file_name.endswith((".jpg", ".jpeg")):
        imwrite(f"{file_base_name}.png", imread(file_name))
    elif file_name.endswith("png"):
        imwrite(f"{file_name}.png", imread(file_name))
    else:
        log.error("File extension is not jpg or jpeg")


def read_image(file_name):
    return imread(file_name)


def write_image(file_name: str, file_data):
    fn = file_name if file_name.endswith(".png") else file_name + ".png"
    imwrite(fn, file_data)


def write_blank_image():
    blank_image = np.zeros((50, 50, 3), np.uint8)
    write_image("blank_black.png", blank_image)


if __name__ == "__main__":
    # convert_file_to_png('DSCN0982.png')
    write_blank_image()
