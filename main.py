import imageIO
import logging
import numpy as np

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


def encode_data_to_image(image, string_to_hide):
    if len(string_to_hide) > image.shape[0] // 8:
        raise ValueError("String to long to encode in the given image")
    bstring = string_to_binary_array(string_to_hide)
    length_in_binary = "{0:016b}".format(len(bstring))
    log.info("Length of bstring= %s", len(bstring))
    data_to_encode = np.append(
        np.array(list(length_in_binary), dtype=np.uint8), bstring
    )
    output_image = image.copy()
    for i in range(len(data_to_encode)):
        output_image[i] = encode_value(image[i], data_to_encode[i])
    return output_image


def decode_data_from_image(input_image) -> str:
    length_of_data_bin_arr = input_image[:16]
    length_of_data_bin = np.bitwise_and(length_of_data_bin_arr, 1)
    op_length_str = ""
    for i in length_of_data_bin:
        op_length_str += str(i)
    output_data_length = int(op_length_str, 2)
    log.info(f"Length of data = {output_data_length}")
    data = input_image[16 : 16 + output_data_length]
    # data = input_image[17 : 17 + (output_data_length * 8)]
    data = np.bitwise_and(data, 1)
    print(data)
    data_str = ""
    for i in range(0, len(data), 8):
        op_length_str = ""
        for j in data[i : i + 8]:
            op_length_str += str(j)
        data_str += chr(int(op_length_str, 2))
    log.info("Data found: " + data_str)
    return data


def main_encode_image(input_image):
    img_shape = input_image.shape
    log.info(f"Input image size= {img_shape}")
    flat_image = convert_img_to_1d_arr(input_image)
    log.info(f"flat_image image size= {flat_image.shape}")

    log.info(f"You can hide at most {input_image.shape[0]//8} characters")
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
    input_image = imageIO.read_image("encoded_image.png")
    main_decode_image(input_image)
