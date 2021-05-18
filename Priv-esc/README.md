## Windows Privilege Escalation

* Note that all the tools will need you to install the **additional libraries with pip**. 
* If the **Useful Info** is checked, read the section below the table.

   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `vulnerable_service.py`| Framework to install a potentially vulnerable service. | Pywin32, Pyinstaller | ⚠️ |
   | `process_monitor.py`| Track process creation and execution. | WMI | ⚠️ |
   | `proc_privileges_monitor.py`| Track process creation, execution and its privileges. | Pywin32, WMI | ⚠️ |
   | `file_monitor.py`| Monitor any changes in the Windows temporary directories | Pywin32 | ⚠️ |
   | `code_injector.py`| Monitors any new files in a specified directory, injects code into them and spawns a reverse shell. | Pywin32 | ⚠️ |

## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `vulnerable_service.py`

* You can use this skeleton framework to create services using Python. 
* It is required you write the scripts you wish to include in your service and save them in a file. It currently run the scripts from the sample script `VulnService_task.vbs`.
* After that, modify the `source_dir` variable with the absolute path of the scripts you just wrote.

<h4>How to create a service executable?</h4>

1. Make sure you have modified the code accordingly. 
2. Use **pyinstaller** to create the service as an .exe: ```C:\> pyinstaller -F --hiddenimport win32timezone vulnerable_service.py```
This command will save the new `vulnerable_service.exe` in the **dist** subdirectory.
3. Change into that directory and install the service: `C:\dist\> vulnerable_service.exe install` 
4. Run/Stop/Remove the service: `C:\dist> vulnerable_service.exe start/stop/remove`
5. If you change the code in `vulnerable_service.py`, you need to create a new executable with *pyinstaller* and reaload the service: `C:\dist> vulnerable_service.exe update`. 

#### `process_monitor.py`

* Monitor the processes executed **without API hooking**. Hence, avoid AV detection. 
* This program uses the [WMI API](http://timgolden.me.uk/python/wmi/tutorial.html) to monitor the process creation event and receive intel of the process: *CommandLine, Time, Executable, Parent PID, PID, User, SID.*
* It will log all this info into a file.
* You can only capture the complete intel of processes created with the same privilege level as you. 
* If you leave the code running for several days, you may find running processes, scheduled tasks, malware, and software updaters. 

#### `proc_privileges_monitor.py`

* Monitor the processes execution with the **WIN32 API** and retrieve their enabled [Token Privileges](https://www.elastic.co/blog/introduction-to-windows-tokens-for-security-practitioners).
* You can only capture the complete intel of processes created with the same privilege level as you. However, I strongly suggest to look for **users with wrong privileges.** 
* It will log all this info into a file.

#### `file_monitor.py`

* The Windows API 'ReadDirectoryChangesW' is used to monitor the **temp** directory for any changes to files or subdirectories.
* You can monitor any additional directory you wish by modifying the `PATHS` variable.
* If you leave the code running for several days, you may find bugs or information disclosures for potential privilege escalations.

#### `code_injector.py`

* This program is built from `file_monitor.py`. Read the info above if you have questions.
* It monitors a directory and checks for file extensions that are typically created by services. 
* Once it finds a service that creates new a file, it will inject some code snippets to the file in order to spawn a reverse shell.
* It will spawn a netcat connection (port 9999) with the privilege level of the originating service. I included a compiled `netcat.exe` for simplicity. 
