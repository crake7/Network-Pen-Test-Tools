<h1 align="center"> Ethical Hacking: Tools 2.0</h1>
<h4 align="center">An NEW assortment of Penetration Testing tools written in Python 3.</h4>

<p align="center">
  <a href="#Requirements">Requirements</a> •
  <a href="#How-to">How To</a> •
  <a href="#Tools">Tools</a> •
  <a href="#Credits">Credits</a>
</p>

___

<h4>Are you looking for additional crafted tools to use during a penetration test?</h4>

This repo is an addition to my previous repo [/Malware-Dev-and-Network-Exploitation-Tools](https://github.com/crake7/Malware-Dev-and-Network-Exploitation-Tools). It brings mostly **NEW tools** to use in a penetration test, as well as **Burp Suite** extensions.


## Requirements

* It is recommended to use the tools in this repository with *virtual environments*. This keeps your projects and its dependencies separate from your main Python installation.
```
$ sudo apt-get install python3-venv
$ sudo mkdir myvirtualenvfolder
$ cd myvirtualenvfolder
~/myvirtualenvfolder$ python3 -m venv virtualv
~/myvirtualenfolderv$ source virtualv/bin/activate
(virtualv) ~/myvirtualenvfolder$ python
```
* An IDE: **VS Code** (suggested) `apt-get install code` or download it [here](https://code.visualstudio.com/download)

* Python 3.6 or higher. Installation depends on your OS, if you need help, click [here](https://realpython.com/installing-python/)

## How-to

1. Download the repo: `$ sudo git clone https://github.com/crake7/Network-Pen-Test-Tools.git`
2. Have a look at the **Tools** section below to check the programs in each folder.
3. Each folder has a **README.md** file that provides additional information for each tool. 

## Tools

* [Networking Tools](/NetworkTools)

   | Program Name | Description|
   | :--------: | :---: |
   | `arper.py`| Your good ol' ARP cache poisoner with host discovery functionality. |
   | `netcat.py`| Simple client-server socket tool to run a shell, upload files and execute a command (Netcat-friendly). |
   | `proxy.py`| TCP proxy to forward and modify traffic, or assess network-based software. |
   | `tcp-client.py`| Basic TCP client to test for services, fuzz, or perform any number of other tasks. |
   | `tcp-server.py`| TCP server to write command shells or crafting a proxy. | 
   | `udp-client.py`| Basic UDP client to test for services, fuzz, or perform any number of other tasks. |

* [SSH Tools](/SSHTools)

   | Program Name | Description|
   | :--------: | :---: |
   | `rforward.py`| Reverse SSH tunneling using Paramiko's demo file with slight modifications. |
   | `ssh_cmd.py`| Avoid dectection making a connection to a SSH server and run a single command. |
   | `ssh_rcmd.py`| Reverse SSH client. It receives commands from an SSH server. Useful for Windows clients. | Paramiko | 
   | `ssh_server.py`| Reverse SSH server. It sends commands to the SSH client(`ssh_rcmd.py`). Useful for Windows clients. | 

* [Sniffers](/Sniffers)

   | Program Name | Description|
   | :--------: | :---: |
   | `host-scanner.py`| UDP host discovery (compatible with Windows/Linux) | 
   | `scapy-mailsniffer.py`| Sniffs traffic and steals email credentials (SMTP, POP3, IMAP). |
   | `sniffer.py`| Reads a single raw packet (compatible with Windows/Linux) | 
   | `sniffer_ip_header_decode.py`| IP Packet sniffer (compatible with Windows/Linux) | 

* [Exfiltration](/Exfiltration)

   | Program Name | Description|
   | :--------: | :---: |
   | `cryptor.py`| Encrypts data and saves it into a file / Decrypts data from a file. | 
   | `email_exfil.py`| Encrypts data and sends it out in an email. (compatible with Windows/Linux) | 
   | `transmit_exfil.py`| Encrypts a file and sends it out via file transfer (compatible with Windows/Linux) | 
   | `paste_exfil.py`| Encrypts data and posts it in Pastebin (compatible with Windows/Linux) |
   | `exfil.py`| Encrypts, decrypts and exilfrates data via email, file transfer or Pastebin. (compatible with Windows/Linux)  |


* [Windows Privilege Escalation](/Priv-esc)

   | Program Name | Description| 
   | :--------: | :---: | 
   | `vulnerable_service.py`| Framework to install a potentially vulnerable service. | 
   | `process_monitor.py`| Tracks process creation and execution. (No API hooking) |
   | `proc_privileges_monitor.py`| Tracks process creation, execution and its privileges. | 
   | `file_monitor.py`| Monitors any changes in the Windows temporary directories. | Pywin32 | 
   | `code_injector.py`| Monitors any new files in a specified directory, injects code into them and spawns a reverse shell. |

## Credits

This repo was created while reading the amazing book: [Black Hat Python 2](https://www.amazon.com/Black-Hat-Python-2nd-Programming/dp/1718501129/ref=sr_1_3?dchild=1&keywords=black+hat+python+2&qid=1618619206&sr=8-3) by Justin Seitz and Tim Arnold. 

Writers and contributors take NO responsibility and/or liability for how you choose to use any of the source code available here. By using any of the files available in this repository, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again, ALL files available here are for EDUCATION and/or RESEARCH purposes ONLY.


## License

The code is licensed under the MIT License.
