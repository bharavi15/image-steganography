import pytest
import main
import numpy as np


def func(original_val, input_val):
    if input_val:
        return original_val | input_val
    else:
        if original_val & 1:
            return original_val ^ 1
        else:
            return original_val


@pytest.fixture
def get_image():
    return np.zeros((50, 50, 3), dtype=np.uint8).ravel()


@pytest.mark.parametrize(
    "original,input,expected",
    [
        (4, 1, 5),
        (4, 0, 4),
        (5, 0, 4),
        (4, 1, 5),
        (0, 1, 1),
        (1, 0, 0),
        (255, 1, 255),
        (254, 1, 255),
        (16, 1, 17),
        (16, 0, 16),
        (17, 0, 16),
    ],
)
def test_bitvalues(original, input, expected):
    actual = main.encode_value(original, input)
    assert actual == expected, "Mismatch found"


@pytest.mark.parametrize("string_to_hide", ["Hello World", "Hello", ""])
def test_encode_decode(get_image, string_to_hide):
    print(get_image)
    main.decode_data_from_image(
        main.encode_data_to_image(get_image, string_to_hide)
    ) == string_to_hide


def test_raises_value_error(get_image):
    s = "abcd" * 7600
    with pytest.raises(ValueError):
        main.encode_data_to_image(get_image, s)
