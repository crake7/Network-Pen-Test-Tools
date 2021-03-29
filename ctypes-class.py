from ctypes import *
import socket
import struct

class IP(Structure):
    ''' [Manadatory] C-based struct that gets external binary data and creates a typical "IP HEADER" structure.
        Ctypes must not specify the endiannes as it shows the machine's natives format and byte order.'''
    _fields_ = [
        ("ihl",         c_ubyte,    4),    # 4-bit unsigned char            Header Length
        ("version",     c_ubyte,    4),    # 4-bit unsigned char            Version
        ("tos",         c_ubyte,    8),    # 1-byte char                    Type of Service (Priority messages)  
        ("len",         c_ushort,   16),   # 2-byte unsigned short          Total Length (Includes IP header and subsequent data)  <---Might want to modify this header ;)
        ("id",          c_ushort,   16),   # 2-byte unsigned short          Identification (Reassembles fragmented packets with this number)
        ("offset",      c_ushort,   16),   # 2-byte unsigned short          Fragment Offset (Stitches fragments together)
        ("ttl",         c_ubyte,    8),    # 1-byte char                    Time-to-live
        ("protocol_num",c_ubyte,    8),    # 1-byte char                    Protocol (What header to look for in transport header)
        ("sum",         c_ushort,   16),   # 2-byte unsigned short          Header checksum (Integrity)                             <---Might want to modify this header ;)
        ("src",         c_uint32,   32),   # 4-byte unsigned int        
        ("dst",         c_uint32,   32),   # 4-byte unsigned int
    ]
    def __new__(cls, socket_buffer=None):
        ''' Fills the __fields__ structure from a raw byte buffer and returns a new instance of the class IP.
            __Init__ will be invoked afterwards.'''
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        ''' Invoked method where "self" is the new instance of the class IP'''
        # Human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))


mypacket = IP(buff)
print(f'{mypacket.src_address} -> {mypacket.dst_address}')