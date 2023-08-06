from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from django.conf import settings

BLOCK_SIZE = 16

def encrypt(message):
    key = settings.ENCRYPTION_KEY.encode("utf-8")
    aes = AES.new(key, AES.MODE_CBC)

    padded_data = pad(message.encode('utf-8'), AES.block_size)
    encrypted_data = aes.encrypt(padded_data)
    return encrypted_data

def decrypt(encrypted_message):
    try:
        key = settings.ENCRYPTION_KEY.encode("utf-8")

        aes = AES.new(key, AES.MODE_CBC)


        decrypted_data = aes.decrypt(encrypted_message)
        unpadded_data = unpad(decrypted_data, AES.block_size)

        return unpadded_data
    

    except Exception as e:
        print(e)
        return None
