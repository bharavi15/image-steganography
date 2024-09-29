import pytest
import main

def func(original_val, input_val):
    if input_val:
        return original_val | input_val
    else:
        if original_val & 1:
            return original_val ^ 1
        else:
            return original_val


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
