## Sniffers

* Note that some tools will need you to download **additional libraries**.
* If the **Useful Info** is checked, read the section below the table.


   | Program Name | Description| Libraries| Useful Info |
   | :--------: | :---: | :---: | :---: | 
   | `host-scanner.py`| Host scanner, compatible with Windows/Linux | struct | ⚠️ |
   | `scapy-mailsniffer.py`| Steals Email Credentials with a sniffer. | scapy |⚠️ |
   | `sniffer.py`| Reads a single raw packet, compatible with Windows/Linux. | | |
   | `ctypes-class.py`| IP class using **ctypes** to read a packet and parses the header info. | N/A | |
   | `struct-class.py`| IP class using **struct** to read a packet and parses the header info. | N/A | |
   | `sniffer_ip_header_decode.py`| IP Packet sniffer compatible with Windows/Linux. | struct | ⚠️ |
   | `sniffer_with_icmp.py`| ICMP Packet sniffer compatible with Windows/Linux. | struct | ⚠️ |

## Useful Info

Some programs may need you to be mindful of additional information. I have included some notes in this section:
   

#### `host-scanner.py`

* The program works by sending UDP datagrams (with a custom message) to all IP's in a network. It takes advantage of the little overhead UDP provides, as well as the fact that most hosts reply back with a ICMP 3, if the probed port is closed. **Beware some hosts might behave differently!**
* This program provides host scanning functionality for Windows and Linux. 
* Do not forget to change the `SUBNET` variable in the script.


#### `scapy-mailsniffer.py`

* **scapy** is a wonderful library that makes packet capturing easy. Use it over **ctypes** and **struct**. 
* This program sniffs packets and captures SMTP, POP3, and IMAP credentials. It filters the packets by using a Berkeley Packet Filter (BPF) filter. Use it with the `-m` or `--mail` flag.
* It also has functionality to display packet contents and dissect protocol information. Use it with the `-s` or `--show` flag. 

#### `sniffer_ip_header_decode.py`

* This is a limited packet sniffer: it will only read in the packets and parse their IP information. 
* It uses the **struct** library, so access to raw sockets is somewhat limited. 
* Beware the functionality changes depending on your OS:
   * Windows - Allows you to see TCP, UDP, and ICMP traffic.
   * Linux   - Allows you to see ICMP packets.
* You can use this program to see the exact route each packet traverses. Very similar use to `traceroute`


#### `ctypes-class.py` vs `struct-class.py`

* Be advice that using the library **scapy** is the easiest option for packet manipulation. 
* The two classes were created only to understand their differences.
* Both libraries can be used to handle binary data into a data structure. 
* *Ctypes* provides a bridge to C-based languages: this enables you to use C-compatible data types and call functions in shared libraries!
* *Struct* converts between Python values and C structs as Python byte objects.
