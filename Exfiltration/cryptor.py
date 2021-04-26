from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA 
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import os
import zlib

def RSA_generate():
    ''' Generate public/private keys for the asymmetric RSA encryption and store them in your current folder.'''
    new_key     = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key  = new_key.publickey().exportKey()

    with open('key.pri', 'wb') as f:
        f.write(private_key)

    with open('key.pub', 'wb') as f:
        f.write(public_key)

def get_RSA_cipher(keytype):
    ''' Helper to grab either of the two RSA keys as needed. Returns the cipher object and the size of the key.'''
    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey  = RSA.importKey(key)
    # Returns an RSA cipher object and the size of the RSA key in bytes
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

def encrypt(plaintext):
    ''' Generates AES key and encrypts it with RSA. It returns the encrypted data.'''
    # Generate AES cipher
    session_key = get_random_bytes(16)
    AES_cipher  = AES.new(session_key, AES.MODE_EAX)

    # Compress plaintext and encrypt it with AES
    compressed_text = zlib.compress(plaintext)
    ciphertext, tag = AES_cipher.encrypt_and_digest(compressed_text)

    # Use RSA public key to encrypt AES session key.
    RSA_cipher, _  = get_RSA_cipher('pub')
    encrypted_session_key = RSA_cipher.encrypt(session_key)

    # The payload to decrypt will include: 
    msg_payload = encrypted_session_key + AES_cipher.nonce + tag + ciphertext

    # Base64 encode it 
    encrypted   = base64.encodebytes(msg_payload)
    return encrypted

def decrypt(encrypted):
    ''' Decrypts the payload and returns the plaintext.'''
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    RSA_cipher, keysize_in_bytes = get_RSA_cipher('pri')

    # Note the session key is derived from the key size of the private key.
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce       = encrypted_bytes.read(16)
    tag         = encrypted_bytes.read(16)
    ciphertext  = encrypted_bytes.read()

    # Decrypt the session key using the RSA key
    session_key = RSA_cipher.decrypt(encrypted_session_key)
    AES_cipher  = AES.new(session_key, AES.MODE_EAX, nonce)
    # Decrypt the message with AES cipher
    decrypted   = AES_cipher.decrypt_and_verify(ciphertext, tag)

    plaintext   = zlib.decompress(decrypted)
    return plaintext

if __name__ == '__main__':

    if (not os.path.isfile('key.pub')) and (not os.path.isfile('key.pri')):
        RSA_generate()
    
    else:
        plaintext = b'Testing functionality.'
        print(decrypt(encrypt(plaintext))) 
