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
    binary_array = np.array([int(bit) for bit in "".join(binary_values)])
    return binary_array


def encode_data_to_image(image, data):
    output_image = image.copy()
    for i in range(len(data)):
        output_image[i] = encode_value(image[i], data[i])
    return output_image


def main(input_image):
    img_shape = input_image.shape
    log.info(f"Input image size= {img_shape}")
    flat_image = convert_img_to_1d_arr(input_image)
    log.info(f"flat_image image size= {flat_image.shape}")
    log.info(f"You can hide at most {flat_image.shape[0]//8} characters")
    string_to_hide = input("Enter the data to be hidden: ")

    bstring = string_to_binary_array(string_to_hide)
    log.info("Length of bstring= %s", len(bstring))
    flat_output_image = encode_data_to_image(flat_image, bstring)
    output_image = flat_output_image.reshape(img_shape)
    imageIO.write_image("encoded_image.png", output_image)
    # # log.info(flat_image.reshape(img_shape))
    # output_image = np.bitwise_xor(flat_image,1)
    # decrypted_image = np.bitwise_xor(output_image,1)
    # # for i in range(flat_image):
    # #     output_image = flat_image[i] & 1
    # log.info(output_image.reshape(img_shape))
    # log.info(decrypted_image.reshape(img_shape))


if __name__ == "__main__":
    input_image = imageIO.read_image("blank_black.png")
    main(input_image)
