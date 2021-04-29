from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA 
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import getpass
import os
import random
import requests
import time
import zlib

# Authentication
username    = input("Enter your Pastebin username: ")
password    = getpass.getpass(prompt='Enter your Pastebin password: ')
api_dev_key = input("Enter your Pastebin API key: ")
# Yahoo web crawler
agent    = 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)' 

def plain_paste(title, contents):
    login_url   = 'https://pastebin.com/api/api_login.php'
    login_data = {
        'api_dev_key':       api_dev_key,
        'api_user_name':     username,
        'api_user_password': password, 
    }
    header = {'User-Agent': agent}
    r = requests.post(login_url, data=login_data, headers=header)
    api_user_key = r.text

    paste_url   = 'https://pastebin.com/api/api_post.php'
    paste_data = {
        'api_paste_name':    title,
        'api_paste_code':    contents.decode(),
        'api_dev_key':       api_dev_key,
        'api_user_key':      api_user_key,
        'api_option':       'paste',
        'api_paste_private': 0,
    }

    r = requests.post(paste_url, data=paste_data, headers=header)
    print(r.status_code)
    print(r.text)

def wait_for_browser(browser):
    ''' Ensures the browser has finished its events and can be used.'''
    # Wait for browser to finish loading and its events have been completed.
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)

def random_sleep():
    ''' Allows the browser to execute tasks that may have not been registered as events by the DOM.
        Makes the browser act as normal user behaviour.'''
    time.sleep(random.randint(5,10))

def login(ie):
    ''' Interacts with the DOM to find all HTML elements required to log in through Internet Explorer.'''
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'loginform-username':
            elem.setAttribute('value', username)
        elif elem.id == 'loginform-password':
            elem.setAttribute('value', password)
    
    random_sleep()
    if ie.Document.forms[0].id == 'w0':
        ie.Document.forms[0].submit()
    wait_for_browser(ie)

def submit(ie, title, contents):
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'postform-name':
            elem.setAttribute('value', title)
        elif elem.id == 'postform-text':
            elem.setAttribute('value', contents)
    
    if ie.document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    random_sleep()
    wait_for_browser(ie)

def ie_paste(title, contents):
    ''' Open an IE instnace, browse to Pastebin and submit your encrypted file.'''

    # Create a new instance of IE COM object
    ie = client.Dispatch('InternetExplorer.Application')
    # Do you want the process to be visible? Debugging = 1, Stealth = 0
    ie.Visible = 0

    ie.Navigate('https://pastebin.com/login', Headers=header)
    wait_for_browser(ie)
    login(ie)

    ie.Navigate('https://pastebin.com/')
    wait_for_browser(ie)
    submit(ie, title, contents.decode())

    ie.Quit()

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
    plaintext = input("Enter the text you want to encrypt, hun: ").encode()
    title     = input("Add a title to your post: ")
    contents = encrypt(plaintext)
    if os.name == 'nt':
        from win32com import client
        ie_paste(title,contents)
    else:
        plain_paste(title, contents)

if __name__ == '__main__':
    # Got your keys? 
    if (not os.path.isfile('key.pub')) and (not os.path.isfile('key.pri')):
        RSA_generate()
    run()

     