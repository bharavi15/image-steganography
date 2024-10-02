import aes
import pytest


# THIS IS SUBJECT TO CHANGE BASED ON CHANGES IN KDF
@pytest.mark.parametrize(
    "password,expected_key_hex",
    [
        ("Helllllllllllooooooooooo Worldddddddddd", "0c649fa5ce5bb2afdf4b63f18f243589"),
        ("Heloo", "3c1b2c1bcd6cbd1c69e2892dd618f2a4"),
        ("a", "ac2d438b03ceb024d5201c47c5aabce7"),
        ("", "d72c87d0f077c7766f2985dfab30e895"),
    ],
)
def test_kdf(password, expected_key_hex):
    assert (
        aes.generate_key_from_password(password).hex() == expected_key_hex
    ), "KDF not working correctly"


@pytest.mark.parametrize(
    "expected_text",
    [
        "Helllllllllllooooooooooo Worldddddddddd",
        "Heloo",
        "a",
        "",
    ],
)
def test_aes_encryption_decryption(expected_text):
    KEY = "Helllo"
    tag, nonce, cipher_text = aes.encrypt(expected_text, KEY)
    actual_text = aes.decrypt(cipher_text, tag, nonce, KEY)
    assert expected_text == actual_text, "Issue with Encryption awa Decryption"
