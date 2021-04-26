## Infiltration

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `cryptor.py`| Your good ol' ARP cache poisoner with host discovery functionality. | Pycryptodomex |⚠ |
   | `email_exfil.py`| Encrypts data and sends it out in an email. (compatible with Windows/Linux) | pycryptodomex | ⚠ |


## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `cryptor.py`

* <strong> Do not forget to add the filenames to </strong>`.gitignore`


#### `email_exfil.py`

* To run the script in **server** mode, you need to add the `-l` flag: `$ python3 netcat.py -t 10.0.0.2 -l -c`
* To run the script in **client** mode, you only need the `-t` and `-p` flags: `$python netcat.py -t 10.0.0.2 -p 5555`
* When you connect a client to a server, the script reads from your STDIN and will continue this way until it receives a end-of-file (EOF) marker. To send the EOF, press `CTRL-D`. This is specially useful when you run a shell. 
