from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA 
from Cryptodome.Random import get_random_bytes

import base64
import ftplib
import io
import os
import socket
import tempfile
import zlib

server   = input("Enter FTP server IP: ")
filepath = input("Enter the path to the file you want to encrypt and send: ")

def plain_ftp(filepath, server='10.0.2.13'):
    ftp = ftplib.FTP(server)
    ftp.login("anonymous", "anon@example.com")
    ftp.cwd('/pub/')
    ftp.storbinary("STOR " + os.path.basename(filepath), open(filepath, "rb"), 1024)
    ftp.quit()
    print(f'File {filepath} sent successfully.')

def transmit(filepath, server='10.0.2.13'):
    '''Windows version'''
    client = socket.socket()
    # Open a port of our choosing
    client.connect((server, 10000))
    
    with open(filepath, 'rb') as f:
        win32file.TransmitFile(
            client, win32file._get_osfhandle(f.fileno()), 0, 0, None, 0, b'', b'')

def get_RSA_cipher(keytype):
    ''' Helper to grab either of the two RSA keys as needed. Returns the cipher object and the size of the key.'''
    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey  = RSA.importKey(key)
    # Returns an RSA cipher object and the size of the RSA key in bytes
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

def RSA_generate():
    ''' Generate public/private keys for the asymmetric RSA encryption and store them in your current folder.'''
    new_key     = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key  = new_key.publickey().exportKey()

    with open('key.pri', 'wb') as f:
        f.write(private_key)

    with open('key.pub', 'wb') as f:
        f.write(public_key)

def encrypt(filepath):
    ''' Generates AES key and encrypts the session key with RSA. It returns the encrypted data.'''
    # Generate AES cipher
    session_key = get_random_bytes(16)
    AES_cipher  = AES.new(session_key, AES.MODE_EAX)

    # Encrypt file contents and compress it.
    with open(filepath, 'rb') as f:
        original = f.read()

    compressed_text = zlib.compress(original)
    ciphertext, tag = AES_cipher.encrypt_and_digest(compressed_text)

    # Use RSA public key to encrypt AES session key.
    RSA_cipher, _  = get_RSA_cipher('pub')
    encrypted_session_key = RSA_cipher.encrypt(session_key)

    # The payload to decrypt will include the contents of the file. 
    msg_payload = encrypted_session_key + AES_cipher.nonce + tag + ciphertext

    # Base64 encode it 
    encrypted   = base64.encodebytes(msg_payload)
    # print(f'This is the encrypted variable: {encrypted}')
    return encrypted

def data_to_file(encrypted):
    ''' Helper to save the encrypted data in different ways'''

    # Do you want to save the encrypted file with a visible name in the file system?
    permanent = tempfile.NamedTemporaryFile(suffix = '.encrypted' , delete = False)
    permanent.write(encrypted)
    return permanent.name

def run():
    encrypted_data = encrypt(filepath)
    encrypted_filepath = data_to_file(encrypted_data)

    if os.name == 'nt':
        import win32file
        transmit(encrypted_filepath)
    else:
        plain_ftp(encrypted_filepath)


if __name__ == "__main__":
    if (not os.path.isfile('key.pub')) and (not os.path.isfile('key.pri')):
        RSA_generate()
    run()