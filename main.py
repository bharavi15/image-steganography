import imageIO
import logging
import numpy as np
import argparse
import aes
from FileInformation import FileInfo

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger()


def convert_img_to_1d_arr(img):
    return img.ravel()


def encode_value(original_val, input_val):
    if input_val:
        return original_val | input_val
    else:
        if original_val & 1:
            return original_val ^ 1
        else:
            return original_val


def string_to_binary_array(s):
    # Convert each character in the string to its binary ASCII value
    binary_values = [format(ord(char), "08b") for char in s]
    # Create a NumPy array from the binary values
    log.info("binval %s", binary_values)
    binary_array = np.array(
        [int(bit) for bit in "".join(binary_values)], dtype=np.uint8
    )
    return binary_array


def binary_array_to_string(data):
    data_str = ""
    for i in range(0, len(data), 8):
        op_length_str = ""
        for j in data[i : i + 8]:
            op_length_str += str(j)
        data_str += chr(int(op_length_str, 2))
    return data_str


def bytes_to_binary_array(b: bytes | bytearray | str):
    to_convert = b
    if isinstance(b, str):
        to_convert = bytearray(b, "utf-8")
    elif isinstance(b, bytes):
        to_convert = bytearray(b)
    converted_list = list(to_convert)
    binary_values = [format(i, "08b") for i in converted_list]
    binary_array = np.array(
        [int(bit) for bit in "".join(binary_values)], dtype=np.uint8
    )
    return binary_array


def encode_data_to_image(image, string_to_hide):
    fileInfo = FileInfo(string_to_hide)
    data_to_encode = fileInfo.serialize()
    output_image = image.copy()
    for i in range(len(data_to_encode)):
        output_image[i] = encode_value(image[i], data_to_encode[i])
    return output_image


def decode_data_from_image(input_image) -> str:
    data_str = FileInfo.deserialize(input_image)
    log.info("Data found: " + data_str)
    return data_str


def main_encode_image(input_image):
    img_shape = input_image.shape
    log.info(f"Input image size= {img_shape}")
    flat_image = convert_img_to_1d_arr(input_image)
    log.info(f"flat_image image size= {flat_image.shape}")

    log.info(f"You can hide at most {flat_image.shape[0]//8} characters")
    string_to_hide = input("Enter the data to be hidden: ")

    flat_output_image = encode_data_to_image(flat_image, string_to_hide)

    output_image = flat_output_image.reshape(img_shape)
    imageIO.write_image("encoded_image.png", output_image)


def main_decode_image(input_image):
    img_shape = input_image.shape
    log.info(f"Input image size= {img_shape}")
    flat_image = convert_img_to_1d_arr(input_image)
    log.info(f"flat_image image size= {flat_image.shape}")
    decode_data_from_image(flat_image)


if __name__ == "__main__":
    # input_image = imageIO.read_image("DSCN0982.png")
    # main_encode_image(input_image)
    parser = argparse.ArgumentParser()
    parser.add_argument("--encode", action=argparse.BooleanOptionalAction)
    parser.add_argument("--decode", action=argparse.BooleanOptionalAction)
    parser.add_argument("--image")
    args = parser.parse_args()

    print(len(bytes_to_binary_array(aes.generate_key_from_password("a"))))
    if args.encode:
        img = args.image or "blank_black.png"
        input_image = imageIO.read_image(img)
        main_encode_image(input_image)
    elif args.decode:
        img = args.image or "encoded_image.png"
        input_image = imageIO.read_image("encoded_image.png")
        main_decode_image(input_image)
    else:
        print("Invalid input")
