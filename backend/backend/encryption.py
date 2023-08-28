from Crypto import Random
from base64 import b64encode, b64decode
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
import environ

env = environ.Env()
environ.Env.read_env()

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self):
        self.key = env('ENCRYPTION_KEY').encode('utf-8')

    def encrypt( self, raw ):
        raw = pad(raw.encode('utf-8'), AES.block_size)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return b64encode( iv + cipher.encrypt( raw ) ).decode('utf-8')

    def decrypt(self, enc ):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ), AES.block_size).decode('utf-8')
