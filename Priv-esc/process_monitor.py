import wmi


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

            process_log_message = (
                f'{cmdline} , {create_date} , {executable} ,'
                f'{parent_pid} , {pid} , {proc_owner} , {owner_sid}'
                )
            print(process_log_message)
            print()
            log_to_file(process_log_message)
        except Exception:
            pass
        
if __name__ == '__main__':
    monitor()
