from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from io import BytesIO


def generate_key_from_password(password: str) -> bytes:
    key = scrypt(password, salt="", key_len=16, N=2**14, r=8, p=1)
    print("key", key.hex())
    return key


def encrypt(plain_text: str, key: str | bytes = None):
    if key is None:
        key = input("Enter Encryption Key:")
    if isinstance(key, str):
        key = generate_key_from_password(key)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
    nonce = cipher.nonce
    print('CipherText:',ciphertext.hex(),'type:',type(ciphertext),' Length',len(ciphertext))
    print('Tag:,',tag.hex(),'type:',type(tag),' Length',len(tag))
    print('Nonce:,',nonce.hex(),'type:',type(ciphertext),' Length',len(nonce))

    return tag, nonce, ciphertext


def decrypt(ciphertext: bytes, tag: bytes, nonce, key: str | bytes=None) -> str:
    if key is None:
        key = input("Enter Decryption Key:")
    if isinstance(key, str):
        key = generate_key_from_password(key)
    
    print('CipherText:',ciphertext.hex(),'type:',type(ciphertext),' Length',len(ciphertext))
    print('Tag:,',tag.hex(),'type:',type(tag),' Length',len(tag))
    print('Nonce:,',nonce.hex(),'type:',type(ciphertext),' Length',len(nonce))

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    message = cipher.decrypt_and_verify(ciphertext, tag)
    print("Message:", message.decode())
    return message.decode()


if __name__ == "__main__":
    tag,nonce,cipher_text = encrypt("")
    decrypt(cipher_text, tag, nonce)
