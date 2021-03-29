import ipaddress
import struct

class IP:
    ''' The struct module provides format characters to specify the sctructure of the binary data.
        We use these format characters to represent the "IP HEADER" '''
    def __init__(self, buff=None):
        # Unpack the buffer according to the format string:
        #            "<"  : Little-endian (Kali x64)
        #            "B"  : 1-byte, Unsigned char
        #            "H"  : 2-byte, Unsigned short
        #            "4s" : 4-byte, char[4]                
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        # struct has not format char for a nibble(4-bit)
        
        self.ver          = header[0] >> 4          # Version
        self.ihl          = header[0] & 0xF         # IP Header Length
        self.tos          = header[1]               # Type of Service (Priority messages)
        self.len          = header[2]               # Total Length (Includes IP header and subsequent data)         <---Might want to modify this header ;)
        self.id           = header[3]               # Identification (Reassembles fragmented packets with this number)
        self.offset       = header[4]               # Fragment Offset (Stitches fragments together)
        self.ttl          = header[5]               # Time-to-live
        self.protocol_num = header[6]               # Protocol (What header to look for in transport header)
        self.sum          = header[7]               # Header checksum (Integrity)                                   <---Might want to modify this header ;)
        self.src          = header[8]               # Source IP
        self.dest         = header[9]               # Destination IP

        # Human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol constants to their names
        self.protcol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

