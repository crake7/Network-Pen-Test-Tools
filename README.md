<h1 align="center"> Ethical Hacking: Tools 2.0</h1>
<h4 align="center">An NEW assortment of Penetration Testing tools written in Python 3.</h4>

<p align="center">
  <a href="#Requirements">Requirements</a> •
  <a href="#How-to">How To</a> •
  <a href="#Tools">Tools</a> •
  <a href="#Useful-Info">Useful Info</a> •
  <a href="#Credits">Credits</a>
</p>

___

<h4>Are you looking for additional crafted tools to use during a penetration test?</h4>

This repo is an addition to my previous repo [/Malware-Dev-and-Network-Exploitation-Tools](https://github.com/crake7/Malware-Dev-and-Network-Exploitation-Tools). It brings mostly **NEW tools** to use in a penetration test as well as **Burp Suite** extensions.


## Requirements

* It is recommended to use this repository using a *virtual environment*. This keep your project and its dependencies separate from your main Python installation.
```
$ sudo apt-get install python3-venv
$ sudo mkdir myvirtualenvfolder
$ cd myvirtualenvfolder

~/myvirtualenvfolder$ python3 -m venv virtualv
~/myvirtualenfolderv$ source virtualv/bin/activate
(virtualv) ~/myvirtualenvfolder$ python
```
* An IDE: **VS Code** suggested: `apt-get install code` or download it [here](https://code.visualstudio.com/download)

* Python 3.6 or higher. Installation depends on your OS, if you need help, click [here](https://realpython.com/installing-python/)

## How-to

1. Download the repo: `$ sudo git clone https://github.com/crake7/Network-Pen-Test-Tools.git`
2. Check the **Tools** section below to learn about each tool.
3. Note that some tools will need you to download additional libraries. 
4. If the **Useful Info** is checked, read the **Useful Info** section below the table.

## Tools

* <h3>Networking Tools</h3>

   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `tcp-client.py`| Basic TCP client to test for services, fuzz, or perform any number of other tasks. | N/A | |
   | `udp-client.py`| Basic UDP client to test for services, fuzz, or perform any number of other tasks. | N/A ||
   | `tcp-server.py`| TCP server to write command shells or crafting a proxy. | N/A ||
   | `netcat.py`| Simple client-server socket tool to run a shell, upload files and execute a command (Netcat-friendly). | N/A | ⚠️ |
   | `proxy.py`| TCP proxy to forward and modify traffic, or assess network-based software. | N/A ||
   | `ssh_cmd.py`| Avoid dectection making a connection to an SSH server and run a single command. | Paramiko | ⚠️ |



## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:

`netcat.py` 

* To run the script in **server** mode, you need to add the `-l` flag: `$ python3 netcat.py -t 10.0.0.2 -l -c`
* To run the script in **client** mode, you only need the `-t` and `-p` flags: `$python netcat.py -t 10.0.0.2 -p 5555`
* When you connect a client to a server, the script reads from your STDIN and will continue this way until it receives a end-of-file (EOF) marker. To send the EOF, press CTRL-D: `CTRL-D`. This is specially useful when you run a shell. 


`ssh_cmd.py`

* fsdfsdf
