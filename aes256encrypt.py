from base64 import b64encode, b64decode
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import kmskey


def encrypt(plain_text, secrt):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)
    print(type(salt))
    #p_key = b'\x83\xe2%\tB\x99\xc0d\x13\x05\x1f>\xaaB\x05\x8e\r\x94T\xe4M\x00)c\x1f\xab+\xb3\xd4\xf3E\xcc.'
    encrContxt = { 'context': secrt[2:5] }
    p_key = kmskey.getEncryptkey(encrContxt)
    private_key = hashlib.scrypt(
         p_key[1], salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM) #nonce= nonce
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        'key': b64encode(p_key[0]).decode('utf-8')
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

