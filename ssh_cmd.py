import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    ''' Connects to an SSH server and runs a single command'''
    client = paramiko.SSHClient()

    # Paramiko supports key authentication, as well ass password authentication:
    # Set policy to auto add and save the hostname and new host key to the local 
    # HostKeys objects
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    
    _,stdout, stderr = client.exec_command(cmd)
    output           = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())
    
if __name__ == '__main__':
        # Getpass looks at the current environment
        import getpass
        # user    = getpass.getuser()
        user      = input('Username: ')
        password  = getpass.getpass()   # Does not show it on terminal

        ip      = input('Enter SSH server IP: ') or '10.0.2.13'
        port    = input('Enter port or <CR>: ') or 2222
        cmd     = input('Enter command or <CR>: ') or 'id'
        ssh_command(ip,port, user, password, cmd)
