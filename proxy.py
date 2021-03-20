import sys
import socket
import threading

# String with ASCII-printable chars or a dot. 
HEX_FILTER = ''.join(
    [(len(repr(chr(integer))) == 3) and chr(integer) or '.' for integer in range(256)])  # The representation of a printable character has a length of 3

def hexdump(src, length=25, show=True):
        '''Prints a hexdump as well as its ASCII characters.'''
        if isinstance(src,bytes):
            src = src.decode()
        
        results = list()

        # Create 16-chars long strings
        for letter in range(0, len(src), length):
            word = str(src[letter:letter+length])

            ascii_printable = word.translate(HEX_FILTER)
            # Return integers representing the Unicode characters in hex number
            hexa = ''.join([f'{ord(c):02x}' for c in word])
            hexwidth        = length*3
            # Hex of index of first byte     Hex value of word   ASCII
            results.append(f'{letter:04x}\t\t{hexa:<{hexwidth}}{ascii_printable}')
                                             # Forces the field
                                             # to be left-aligned 
        if show:
            for line in results:
                print(line)
        else:
            return results

def receive_from(connection):
    ''' Watch communication in real time from local or remote data.
        It is used for both sides of the communication              '''
    buffer = b""
    connection.settimeout(5)        # Evaluates the connection every 5 seconds; modify accordingly.
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def request_handler(buffer):
    # perform packet modifications
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    print("Connected to remote host on %s:%d" % (remote_host,remote_port))

    # First, check if it is needed to initiatie a connection to the remote side and request data,
    # some server daemons expect this such as the FTP server. 
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[+] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)
    
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[-] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[+] Sent to remote socket.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer): 
            print( "[-] Received %d bytes from remote socket." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[+] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    ''' Set up and manage the proxy connection in local host'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind to the local host and listen
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("There was a problem on bind: %r" % e)

        print("[!] Failed to listen on %s:%d" % (local_port,local_port))
        print("[!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target = proxy_handler,
            args   = (client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()
    
def main():
    if len(sys.argv[1:]) != 5:
        print(f"Usage:  \t./proxy.py\t[localhost]\t[local port]", end="")
        print(f"\t[remote host]\t[remote port]\t[receive_first]")
        print(f"Example:\t./proxy.py\t127.0.0.1\t9000\t\t10.12.132.1\t9000\t\tYas")
        sys.exit(0)
    local_host   = sys.argv[1]
    local_port   = int(sys.argv[2])

    remote_host  = sys.argv[3]
    remote_port  = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "Yas" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()




