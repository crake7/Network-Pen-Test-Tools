import argparse
import socket
import shlex    # Might be useful only for Unix-like shells. 
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

    return output.decode()

class NetCat:
    def __init__(self, args, buffer = None):
        ''' Initialize NetCat object with arguments from cmmd line, the buffer, and create a socket object.'''
        self.args    = args
        self.buffer  = buffer
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Overcome the "Address already in use" by manipulating options at the socket level
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        ''' Send data from stdin as bytes'''
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data      = self.socket.recv(4096)
                    recv_len  = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer  = input('> ')
                    buffer += '\n'      
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit
    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        
        while True:
            client_socket, _ = self.socket.accept()
            client_thread    = threading.Thread(
                target = self.handle,
                args   = (client_socket,)
            )
            client_thread.start()
    
    def handle(self, client_socket):
        ''' Executes commands according to the arguments it receives '''
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as files:
                files.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            ''' Start an interactive shell. As scripts reads from STDIN, you must send EOF (Ctrl+D) maker
            to start it.'''
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'Sassy: #> ')
                    while '\n' not in cmd_buffer.decode():      # Netcat friendly (0x0a)
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()





# Block 'main' to handle command line arguments and call the functions
if __name__ == '__main__':
    parser  = argparse.ArgumentParser(

        # Text to display before the argument 
        description     = 'Da Sassiest Network Tool', 

        # Implies 'description' and 'epilog' are already correctly formatted and shouldn't be line-wrapped
        formatter_class = argparse.RawDescriptionHelpFormatter,
        
        # Text to display after the argument --help
        epilog          = textwrap.dedent('''Example:
               netcat.py -t 192.168.0.1 -p 6969                                    # Connect to server
               netcat.py -t 192.168.0.1 -p 6969 -l -c                              # Set up interactive Shell
               netcat.py -t 192.168.0.1 -p 6969 -l -u = uploadfile.txt             # Upload file
               netcat.py -t 192.168.0.1 -p 6969 -l -e = \"cat /etc/passwd\"          # Execute a command
echo 'ABC' | ./netcat.py -t 192.168.0.1 -p 6969                                    # Echo text to server
        '''))
    parser.add_argument ('-c', '--command', action  = 'store_true',         help = 'set up a shell')
    parser.add_argument ('-e', '--execute', help    = 'execute specified command')
    parser.add_argument ('-l', '--listen',  action  = 'store_true',         help = 'listen')
    parser.add_argument ('-p', '--port',    type    = int, default = 6969,  help = 'target port')
    parser.add_argument ('-t', '--target',  default = '192.168.0.1',        help = 'target IP')
    parser.add_argument ('-u', '--upload',  help    = 'upload file')
    args = parser.parse_args()
    
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
        
    nc = NetCat(args, buffer.encode())
    nc.run()

