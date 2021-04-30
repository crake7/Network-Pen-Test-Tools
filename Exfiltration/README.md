## Exfiltration

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `cryptor.py`|  Encrypts data and saves it into a file / Decrypts data from a file.   | Pycryptodomex |⚠ |
   | `email_exfil.py`| Encrypts data and sends it out in an email. (compatible with Windows/Linux) | pycryptodomex | ⚠ |
   | `transmit_exfil.py`| Encrypts a file and sends it out via file transfer (compatible with Windows/Linux) | Pycryptodomex |⚠ |
   | `paste_exfil.py`| Encrypts data and posts it in Pastebin (compatible with Windows/Linux) | Pycryptodomex |⚠ |
   | `exfil.py`| Encrypts, decrypts and exilfrates data via email, file transfer or Pastebin. (compatible with Windows/Linux)  | Pycryptodomex |⚠ |




## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:

* <strong> Do not forget to add the RSA key pair filenames to </strong>`.gitignore` 
* All the tools here use hybrid encryption. You can read `cryptor.py` to have an idea of how it does it.
   
  
#### `cryptor.py`

* This program will begin by creating a public/private RSA key pair to encrypt/decrypt your AES key and the ciphertext.
* The program will use AES to encrypt the data you want to exfiltrate and save it on a file.
* The encrypted data will be saved base64-encoded.
* You can also decrypt the data you previously saved by providing its filename. 

#### `email_exfil.py`

* The program will encrypt the data you provide, and will email it to an account depending on your OS:
  * It will use *Outlook* if you are using Windows.
  * It will use *Google's SMTP* if you are using anything else.
* Make sure you Enable **Less Secure Apps**. Confused? Info [here](https://www.slipstick.com/outlook/outlook-gmails-secure-apps-setting/)


#### `transmit_exfil.py`

* The program will encrypt the data from a file, dump it into a new file in the **/tmp** directory, and will send it via file transfer depending on your OS:
  * It will *open a socket and send the file to port 10000* if you are using *Windows*.
  * It will use *FTP* if you are using anything else.
* FTP Server Checklist [(help)](https://likegeeks.com/ftp-server-linux/): 
   * Allow Anonymous FTP access
   * Create the **pub/** directory 
   * Allow Anonymous users to upload files.

#### `paste_exfil.py`

* You need to sign up to [Pastebin](https://pastebin.com/signup) to use this program!!
* This program logs in your **Pastebin** account and posts your encrypted data there. It will do it differently based on your OS:
   * It will *create an instance of a Internet Explorer COM object and use the DOM* if you are using *Windows*.
   * It will use the *Pastebin [API](https://pastebin.com/doc_api)* if you are using anything else.

#### `exfil.py`

* This tool combines all the functionality from the programs above:
   * Encrypts/decrypts data,
   * Exfiltrates encrypted data via email,
   * Exfiltrates encrypted data via file transfer,
   * Exfiltrates encrypted data posting it in Pastebin.
* Read any of the tools above, if needed.

