import numpy as np
import logging
import aes

log = logging.getLogger()
IS_ENCRYPTION_ENABLED = True
TAG_LENGTH = 16 * 8
NONCE_LENGTH = 16 * 8


class FileInfo:
    def __init__(self, data: str) -> None:
        if len(data) == 0:
            raise ValueError("Empty string")
        self.data = data
        if IS_ENCRYPTION_ENABLED:
            tag, nonce, cipher_text = aes.encrypt(self.data, "")
            self.data_bytes = b"".join([tag, nonce, cipher_text])
        else:
            self.data_bytes = data.encode()
        self.data_bin_arr = self.to_binary_arr()
        print("Length of data=", len(self.data_bin_arr))
        self.data_bin_arr_length = "{0:016b}".format(len(self.data_bin_arr))

    def to_binary_arr(self):
        converted_list = list(self.data_bytes)
        binary_values = [format(i, "08b") for i in converted_list]
        binary_array = np.array(
            [int(bit) for bit in "".join(binary_values)], dtype=np.uint8
        )
        return binary_array

    def serialize(self):
        serialized = np.append(
            np.array(list(self.data_bin_arr_length), dtype=np.uint8), self.data_bin_arr
        )
        print("Final Length = ", len(serialized))
        return serialized

    @staticmethod
    def binary_array_to_string(data):
        data_str = ""
        for i in range(0, len(data), 8):
            op_length_str = ""
            for j in data[i : i + 8]:
                op_length_str += str(j)
            data_str += chr(int(op_length_str, 2))
        return data_str

    @staticmethod
    def deserialize(arr):
        length_of_data_bin_arr = arr[:16]
        length_of_data_bin = np.bitwise_and(length_of_data_bin_arr, 1)
        op_length_str = ""
        for i in length_of_data_bin:
            op_length_str += str(i)
        output_data_length = int(op_length_str, 2)

        log.info(f"Length of data = {output_data_length}")
        data = arr[16 : 16 + output_data_length]
        tag = data[:TAG_LENGTH]
        print("data", len(data))
        print("tag", len(tag))
        tag = np.bitwise_and(tag, 1)
        b = "".join([str(x) for x in tag])
        tag = int(b, 2).to_bytes(16, byteorder="big")
        print("tag data", tag.hex())

        nonce = data[TAG_LENGTH : TAG_LENGTH + NONCE_LENGTH]
        nonce = np.bitwise_and(nonce, 1)
        print("nonce", len(nonce))
        b = "".join([str(x) for x in nonce])
        nonce = int(b, 2).to_bytes(16, byteorder="big")
        print("nonce data", nonce.hex())

        cipher_text = data[TAG_LENGTH + NONCE_LENGTH : output_data_length]
        cipher_text = np.bitwise_and(cipher_text, 1)
        print("cipher_text", len(cipher_text))
        b = "".join([str(x) for x in cipher_text])
        cipher_text = int(b, 2).to_bytes(len(cipher_text) // 8, byteorder="big")
        print("cipher_text data", cipher_text.hex())

        # cipher_text = FileInfo.binary_array_to_string(cipher_text).encode()
        data = aes.decrypt(cipher_text, tag, nonce, "")
        return data
