from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import kmskey
from vkdatabaseconnect import getPasswordData


def encrypt(plain_text, secrt):
    # salt = get_random_bytes(AES.block_size)
    # encrContxt = { 'context': secrt[0:2] }
    # c_key, p_key = kmskey.getEncryptkey(encrContxt)
    # private_key = hashlib.scrypt(
    #      p_key, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    # cipher_config = AES.new(private_key, AES.MODE_GCM) #nonce= nonce
    # cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    # return {
    #     'cipher_text': b64encode(cipher_text).decode('utf-8'),
    #     'salt': b64encode(salt).decode('utf-8'),
    #     'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
    #     'tag': b64encode(tag).decode('utf-8'),
    #     'key': c_key
    # }
    salt = get_random_bytes(AES.block_size)

    encrContxt = { 'context': secrt[0:2] }
    c_key, p_key = kmskey.getEncryptkey(encrContxt)

    private_key = hashlib.scrypt(p_key, salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(plain_text.encode())
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        'key': c_key
    }

def checkpass(secrt):
    response = getPasswordData(secrt)
    # decode the dictionary entries from base64
    salt = b64decode(response[0])
    ciphertext = b64decode(response[1])
    nonce = b64decode(response[2])
    tag = b64decode(response[3])
    enckey = b64decode(response[4])
    encrContxt = { 'context': secrt[0:2] }
    pkey= kmskey.getDecryptkey(enckey, encrContxt)
    private_key = hashlib.scrypt(pkey, salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted.decode('utf-8')
