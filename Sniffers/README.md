## Sniffers

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `sniffer.py`| Reads one raw packet either from Windows/OS. | | |
   | `ctypes-class.py`| IP class using **ctypes** to read a packet and parses the header info. | N/A | ⚠️ |
   | `struct-class.py`| IP class using **struct** to read a packet and parses the header info. | N/A | ⚠️ |


## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   
#### `ctypes-class.py` vs `struct-class.py`

* Be advice that using the library **scapy** is the easiest option for packet manipulation. 
* The two classes were created only to understand their differences.
* Both libraries can be used to handle binary data into a data structure. 
* *Ctypes* provides a bridge to C-based languages: this enables you to use C-compatible data types and call functions in shared libraries!
* *Struct* converts between Python values and C structs as Python byte objects.
