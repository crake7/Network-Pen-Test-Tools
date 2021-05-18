## Windows Privilege Escalation

* Note that all tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `vulnerable_service.py`| Framework to install a potentially vulnerable service. | Pywin32 | ⚠️ |
   | `file_monitor.py`| Monitor any changes in the Windows temporary directories | Pywin32 | ⚠️ |

## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `file_monitor.py`

* The Windows API 'ReadDirectoryChangesW' is used to monitor the **temp** directory for any changes to files or subdirectories.
* You monitor any directory you wish by modifying the `PATHS` variable.
* If you leave the code running for several days, you may find bugs or information disclosures for potential privilege escalations.

#### `vulnerable_monitor.py`

* You can use this framework to install and run services using Python. 
* It is required you write the scripts you wish to include in your service and save them in a file. 
* Modify the `source_dir` variable with the absolute path of your scripts.
* If you leave the code running for several days, you may find bugs or information disclosures for potential privilege escalations.
