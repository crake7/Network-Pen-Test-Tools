import socket
import threading

# Server will listen on this socket
IP   = '0.0.0.0'
PORT = 9998

def main():
    """Create a multi-threaded TCP server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind ((IP, PORT))
    # Queue up to 5 'connect requests' before refusing outside connections.
    server.listen(5)        
    print(f'[+] Listening on {IP}:{PORT}')

    while True:
        # client socket in client variable and remote connection details in address variable
        client, address = server.accept()
        print(f'[+] Accepted connection from {address[0]}:{address[1]}')
        # Start the threads to handle simultaneous client connections. 
        client_handler  = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[+] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()
