from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA 
from Cryptodome.Random import get_random_bytes

import base64
import getpass
import os 
import smtplib
import time
import zlib


# Google's SMTP info
smtp_server   = 'smtp.gmail.com'
smtp_port     = 587

subject       = input('Subject: ')
smtp_acct     = input('From: ')
smtp_password = getpass.getpass()
tgt_accts     = input('To: ')


def plain_email(subject, contents):
    ''' Platform-independant email sender.'''
    message  = f'Subject: {subject}\nFrom {smtp_acct}\n'
    message += f'To: {tgt_accts}\n\n{contents.decode()}'
    server   = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    try:
        server.login(smtp_acct, smtp_password)
        # server.set_debuglevel(1)
        server.sendmail(smtp_acct, tgt_accts, message)
        time.sleep(1)
        print("Email sent successfully.")
        server.quit()
    
    except smtplib.SMTPAuthenticationError as e:
        print(e)
        server.quit()
        
def outlook(subject, contents):
    ''' Windows email sender. '''
    # Use WIN32COM to create an instance of the Outlook application
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body    = contents.decode()
    message.To      = tgt_accts[0]
    message.Send()

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

def run():
    plaintext = b'This is a test.'
    encrypted_message = encrypt(plaintext)

    if os.name == 'nt':
        import win32com.client
        outlook(subject, encrypted_message)
    else:
        plain_email(subject, encrypted_message)

if __name__ == '__main__':

    if (not os.path.isfile('key.pub')) and (not os.path.isfile('key.pri')):
        RSA_generate()

    run()


