## Windows Privilege Escalation

* Note that all tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `vulnerable_service.py`| Framework to install a potentially vulnerable service. | Pywin32, Pyinstaller | ⚠️ |
   | `file_monitor.py`| Monitor any changes in the Windows temporary directories | Pywin32 | ⚠️ |

## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `file_monitor.py`

* The Windows API 'ReadDirectoryChangesW' is used to monitor the **temp** directory for any changes to files or subdirectories.
* You monitor any directory you wish by modifying the `PATHS` variable.
* If you leave the code running for several days, you may find bugs or information disclosures for potential privilege escalations.

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
