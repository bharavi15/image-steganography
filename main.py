import imageIO
import logging
import numpy as np

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
log = logging.getLogger()


if __name__ == "__main__":
    input_image = imageIO.read_image("img.png")
    img_shape = input_image.shape
    log.info(f"Input image size= {img_shape}")
    flat_image = input_image.ravel()
    log.info(flat_image.reshape(img_shape))
    output_image = np.bitwise_xor(flat_image,1)
    decrypted_image = np.bitwise_xor(output_image,1)
    # for i in range(flat_image):
    #     output_image = flat_image[i] & 1
    log.info(output_image.reshape(img_shape))
    log.info(decrypted_image.reshape(img_shape))