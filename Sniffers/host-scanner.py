import ipaddress
import os
import socket
import struct
import sys
import threading
import time

SUBNET  = '192.168.0.0/24'
# Signature to check in ICMP responses
MESSAGE = 'YAAAAAS'

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
        # struct has not format char for a nibble(4-bit):

        #     For the ver variable, you right-shift the byte by 4 places(append
        #     0000) to get the high-order nybble off the first byte 
        self.ver          = header[0] >> 4          # Version

        #     The header length will take the low-order nybble by using 
        #     the boolean AND with 0xF(00001111)
        self.ihl          = header[0] & 0xF         # IP Header Length

        self.tos          = header[1]               # Type of Service (Priority messages)
        self.len          = header[2]               # Total Length (Includes IP header and subsequent data)         <---Might want to modify this header ;)
        self.id           = header[3]               # Identification (Reassembles fragmented packets with this number)
        self.offset       = header[4]               # Fragment Offset (Stitches fragments together)
        self.ttl          = header[5]               # Time-to-live
        self.protocol_num = header[6]               # Protocol (What header to look for in transport header)
        self.sum          = header[7]               # Header checksum (Integrity)                                   <---Might want to modify this header ;)
        self.src          = header[8]               # Source IP
        self.dst          = header[9]               # Destination IP

        # Human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e,self.protocol_num))
            self.protocol = str(self.protocol_num)


class ICMP:
    def __init__(self, buff):
        header    = struct.unpack('<BBHHH', buff)
        self.type = header[0]   # ICMP Type message number
        self.code = header[1]   # Code
        self.sum  = header[2]   # Checksum 
        self.id   = header[3]   # Identifier
        self.seq  = header[4]   # Sequence number 

def udp_sender():
    ''' Sprays out UDP dragrams with the message chosen to port 65212'''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host  = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host,0))
        # Include IP header
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            # Turn NIC into a promiscious girl 
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        # store multiple items in a single variable without duplicates 
        alive_hosts = set([f'{str(self.host)}*'])
        try:
            while True:
                # read a packet
                raw_buffer = self.socket.recvfrom(65535)[0]
                # create an IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    # calculate where our ICMP packet starts in the raw packet. 
                    # IP header ihl field * 32-bit words( 4-byte chunks) = size of IP header
                    offset = ip_header.ihl * 4
                    # The last 8 bytes of the IP header contain the ICMP type and code. (https://www.juniper.net/documentation/images/ICMP2.gif)
                    buf    = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            # Check for MESSAGE
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                target = str(ip_header.src_address)
                                if target != self.host and target not in alive_hosts:
                                    alive_hosts.add(str(ip_header.src_address))
                                    print(f'Host Up: {target}')
            
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
            print('\nUser Interrupted.')
            if alive_hosts:
                print(f'\n\nSummary: Hosts up on {SUBNET}')
            for host in sorted(alive_hosts):
                print(f'{host}')
            print('')
            sys.exit()

# mypacket = IP(buff)
# print(f'{mypacket.src_address} -> {mypacket.dst_address}')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.0.24'

    # SUBNET  = input('Enter the subnet <IP>/<SUBNET>: ')
    # # Signature to check in ICMP responses
    # MESSAGE = input('Enter the string to send in ICMP requests: ')
    
    host_scan = Scanner(host)
    time.sleep(5)
    # Opens a thread to avoid interferance with sniffer
    t = threading.Thread(target=udp_sender)
    t.start()
    host_scan.sniff()

