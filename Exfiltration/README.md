## Exfiltration

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `cryptor.py`| Encrypts and decrypts data using symmetric and assymetric encryption.  | Pycryptodomex |⚠ |
   | `email_exfil.py`| Encrypts data and sends it out in an email. (compatible with Windows/Linux) | pycryptodomex | ⚠ |
   | `transmit_exfil.py`| Encrypts a file and sends it out via file transfer (compatible with Windows/Linux) | Pycryptodomex |⚠ |


## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `cryptor.py`

* This program will begin by creating a public/private RSA key pair to encrypt/decrypt your AES key and the ciphertext.
* <strong> Do not forget to add the RSA key pair filenames to </strong>`.gitignore` 
* The program will use AES to encrypt the data you want to exfiltrate.
* The encrypted data will be sent base64-encoded.

#### `email_exfil.py`

* This program uses hybrid encryption: You can read `cryptor.py` to have a high-level overview of its functionality.
* <strong> Do not forget to add the RSA key pair filenames to </strong>`.gitignore` 
* The program will encrypt the data you provide, and will email it to an account depending on your OS:
  * It will use *Outlook* if you are using Windows.
  * It will use *Google's SMTP* if you are using anything else.
* Make sure you Enable **Less Secure Apps**. Confused? Info [here](https://www.slipstick.com/outlook/outlook-gmails-secure-apps-setting/)


#### `transmit_exfil.py`

* This program uses hybrid encryption: You can read `cryptor.py` to have a high-level overview of its functionality.
* <strong> Do not forget to add the RSA key pair filenames to </strong>`.gitignore` 
* The program will encrypt the data from a file, dump it into a new file in the **/tmp** directory, and will send it via file transfer depending on your OS:
  * It will * open a socket and send the file to port 10000* if you are using *Windows*.
  * It will use *FTP* if you are using anything else.

* Set up for FTP Server correctly, [help](https://likegeeks.com/ftp-server-linux/): 
   * Allow Anonymous FTP access
   * Create the **pub/** directory 
   * Allow Anonymous users to upload files.
