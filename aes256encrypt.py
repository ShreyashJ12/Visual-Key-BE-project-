
# AES 256 encryption/decryption using pycryptodome library

from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt(plain_text, password):
    # generate a random salt
    # salt = get_random_bytes(AES.block_size)
    salt = b64decode('lQL+Et73kRcwG7njMjNQOQ==')
    nonce = b64decode('mqOp8IOrb8gkxn/WhLj9HA==')
    tag = b64decode('Befay3pQd6LBT24G6vmC5A==')

    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM, nonce= nonce)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


hashed_string= 'ff94b76307958c3451f53b44847c299084d5391ff84b8d0dd745ee06f0c4ca61'
print(encrypt(hashed_string, "shreyash"))