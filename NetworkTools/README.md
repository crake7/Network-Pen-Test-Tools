## NetworkTools

* Note that some tools will need you to download additional libraries.
* If the Useful Info is checked, read the Useful Info section below the table.



   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `tcp-client.py`| Basic TCP client to test for services, fuzz, or perform any number of other tasks. | N/A | |
   | `udp-client.py`| Basic UDP client to test for services, fuzz, or perform any number of other tasks. | N/A ||
   | `tcp-server.py`| TCP server to write command shells or crafting a proxy. | N/A ||
   | `netcat.py`| Simple client-server socket tool to run a shell, upload files and execute a command (Netcat-friendly). | N/A | ⚠️ |
   | `proxy.py`| TCP proxy to forward and modify traffic, or assess network-based software. | N/A |⚠️|
   

## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `netcat.py` 

* To run the script in **server** mode, you need to add the `-l` flag: `$ python3 netcat.py -t 10.0.0.2 -l -c`
* To run the script in **client** mode, you only need the `-t` and `-p` flags: `$python netcat.py -t 10.0.0.2 -p 5555`
* When you connect a client to a server, the script reads from your STDIN and will continue this way until it receives a end-of-file (EOF) marker. To send the EOF, press `CTRL-D`. This is specially useful when you run a shell. 


#### `proxy.py`

* The program has messed up the DNS configuration of some users. If you are having networking issues after running the script, verify your name server was not modified: `$ cat /etc/resolv.conf`
