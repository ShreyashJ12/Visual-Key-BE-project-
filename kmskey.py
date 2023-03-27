import boto3
import base64

kms = boto3.client('kms')
key ='arn:aws:kms:ap-south-1:524675107721:key/ccf6b505-3e36-4d11-928e-936455cb82e5'

# The data key to encrypt
def getEncryptkey(encrContext) :
    response = kms.generate_data_key(
        KeyId= key,
        EncryptionContext= encrContext,
        NumberOfBytes=32
    )
    ciphertext = base64.b64encode(response['CiphertextBlob'])
    plaintext = base64.b64encode(response['Plaintext'])
    return ciphertext, plaintext

def getDecryptkey(ciphertext, encrContext) :
    response = kms.decrypt(
        CiphertextBlob= ciphertext,
        EncryptionContext= encrContext,
        KeyId = key
    )

    # The plaintext data key
    plaintext_key = response['Plaintext']
    p_key = base64.b64encode(plaintext_key)
    return p_key