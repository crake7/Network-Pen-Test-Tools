## SSHTools

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.



   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `rforward.py`| Reverse SSH tunneling using Paramiko's demo file with slight modifications. | Paramiko ||
   | `ssh_cmd.py`| Avoid dectection making a connection to a SSH server and run a single command. | Paramiko | ⚠️ |
   | `ssh_rcmd.py`| Reverse SSH client. It receives commands from an SSH server. Useful for Windows clients. | Paramiko | ⚠️ |
   | `ssh_server.py`| Reverse SSH server. It sends commands to the SSH client(`ssh_rcmd.py`). Useful for Windows clients. | Paramiko | ⚠️ |
   | `test_rsa.key`| Sample server host key provided by Paramiko. |N/A||


## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:

#### `rforward.py`

* This script is useful to access a blocked resource in a network by connecting to your own SSH server from a SSH client:
`$ python3 rforward.py <SSHserverIp> -p <port> -r <BlockIp>:<port> --user=<username> --password`

#### `ssh_cmd.py`

* You can download paramiko [here](https://github.com/paramiko/paramiko/)
* This program connects to your SSH server and runs a command. Do not forget to set up your own SSH server!
* Paramiko supports authentication with keys as well. It is recommended to **only use SSH key autehntication** in a real engagement.


#### `ssh_rcmd.py`

* You can download paramiko [here](https://github.com/paramiko/paramiko/)
* This program runs commands on Windows clients over SSH by receiving commands from an SSH server.
* Use this script with `ssh_server.py`
* Paramiko supports authentication with keys as well. It is recommended to only use **SSH key autehntication** in a real engagement.


#### `ssh_server.py`

* You can download paramiko [here](https://github.com/paramiko/paramiko/)
* Use this script with `ssh_rcmd.py`. 
* The SSH key the server is using was originally downloaded from the paramiko repository. For convenience, I included it as a separate file: `test_rsa.key`. Type this filename when you are prompted to input *HOSTKEY file name:* or use your own key. 
