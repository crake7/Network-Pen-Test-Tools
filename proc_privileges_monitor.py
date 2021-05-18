import os
import sys
import win32api
import win32con
import win32security
import wmi


def get_process_privileges(pid):
    ''' Automatically retrieves the enabled privileges on the processes we monitor'''
    try: 
        hproc = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION, False, pid          # PID used to obtain a process handle
            )
        htok  = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        privs = win32security.GetTokenInformation(
            htok, win32security.TokenPrivileges
            ) 
        privileges = ''
        # Privilege / Enabled(Y/N) 
        for priv_id, flags in privs:
            # Check enabled bits
            if flags == (win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT):
                privileges += f'{win32security.LookupPrivilegeName(None, priv_id)} |'
    except Exception:
        privileges = 'N/A'
    
    return privileges

def log_to_file(message):
    with open('process_monitor_log.csv', 'a') as fd:
        fd.write(f'{message}\r\n')

def monitor():
    head = 'CommandLine, Time, Executable, Parent PID, PID, User, SID, Privileges'
    log_to_file(head)
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')   # Returns a 'New Process' event
    while True:
        try:
            new_process = process_watcher()         # The event is a Win32_Process WMI class
            cmdline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()
            owner_sid = new_process.GetOwnerSid()

            privileges  = get_process_privileges(pid)
            process_log_message = (
                f'{cmdline} , {create_date} , {executable} ,'
                f'{parent_pid} , {pid} , {proc_owner} , {owner_sid} , {privileges}'
                )
            print(process_log_message)
            print()
            log_to_file(process_log_message)
        except Exception:
            pass
        
if __name__ == '__main__':
    monitor()