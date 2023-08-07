from Crypto import Random
from base64 import b64encode, b64decode
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
import environ

env = environ.Env()
environ.Env.read_env()

# BLOCK_SIZE = 16

# # def unpad(data):
# #     return data[:-ord(data[-1])]

# def encrypt(message):
#     IV = Random.new().read(BLOCK_SIZE)
#     aes = AES.new(env("ENCRYPTION_KEY").encode("utf8"), AES.MODE_CBC, IV)
#     return b64encode(IV + aes.encrypt(pad(message.encode('utf-8'), BLOCK_SIZE))).decode('utf-8')

# def decrypt(encrypted):
#     # encrypted = b64decode(encrypted)
#     # IV = encrypted[:BLOCK_SIZE]
#     # aes = AES.new(env("ENCRYPTION_KEY").encode("utf8"), AES.MODE_CBC, IV)
#     # return unpad(aes.decrypt(encrypted[BLOCK_SIZE:]), BLOCK_SIZE).decode('utf-8')


#     # iv = b64decode(encrypted)[:16]
#     # ciphertext = b64decode(encrypted)[16:]
#     # cipher = AES.new(env("ENCRYPTION_KEY").encode("utf8"), AES.MODE_CBC, iv)
#     # print(cipher.decrypt(ciphertext))
#     # plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
#     # print(plaintext)
#     # return plaintext
#     ciphertext = 'BQ4cLyMyJdIFv2plxZhCsx2oC/BxYJbdXlLO/bCAEeg='
#     key = b'aPdSgVkYp3s6v9y$B?E-H+MbQeThWmZq'
#     iv = b64decode(ciphertext)[:16]
#     ct = b64decode(ciphertext)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     print(len(cipher.decrypt(ct)))
#     plaintext = unpad(cipher.decrypt(ct), BLOCK_SIZE).decode('utf-8')
#     print(plaintext) # prints the decrypted plaintext


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
