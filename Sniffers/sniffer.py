import socket
import os

HOST   = input('Enter your local ip address: ')

def main():
    # create a socket protocol depending on OS
    if os.name == 'nt':
        # Windows allows to sniff all incoming packets regardless of protocol
        socket_protocol = socket.IPPROTO_IP
    else:
        # Linux forces to specify we are sniffing ICMP packets, boo hoe! 
        socket_protocol = socket.IPPROTO_ICMP

        # Initialize the raw socket
    try:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind ((HOST,0))
        # Include the IP header in the capture
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except PermissionError as e:
        print("[!!] PERMISSION ERROR: Do you even root, bro?")
        return

    # Turn on promiscuous mode in Windows OS
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    # read one packet
    print(sniffer.recvfrom(65565))

    # if we're on Windows, turn off promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.rcval_off)

if __name__ == '__main__':
    main()