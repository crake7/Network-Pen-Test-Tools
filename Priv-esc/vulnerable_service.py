import os
import servicemanager          # Interfaces with the Windows Service Control Manager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil         # Handles Windows services

source_dir = 'C:\\Network-Pen-Test-Tools\\Priv-Esc'                                         # MODIFY ME
target_dir = 'C:\\Windows\\Temp'

# Uses a base class to create vulnerable services
class VulnSvc(win32serviceutil.ServiceFramework):
    _svc_name_         = "VulnerableService"
    _svc_display_name_ = "A vulnerable service"
    _svc_description_  = ("Executes VBScripts at regular intervals." + 
                            "What could possibly go wrong, hun?")
    
    def __init__(self, args):
        ''' Creator of the Windows Service '''
        self.vbs      = os.path.join(target_dir, "VulnService_scripts.vbs")                 # MODIFY ME
        self.timeout  = 1000 * 60

        # Initialize the framework
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Creates a handle for your waitable event 
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcStop(self):
        ''' Called when the service is asked to stop '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
    
    def SvcDoRun(self):
        ''' Called when the service is asked to start. '''
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()
    
    def main(self):
        ''' Every minute, copy the script file, execute it and removie it.'''
        while True:
            # Returns when an event is signalled(after the 1 min you specified)
            event_type = win32event.WaitForSingleObject(
                self.hWaitStop, self.timeout)
            # Stop the loop when the service receives the STOP signal
            if event_type == win32event.WAIT_OBJECT_0:
                servicemanager.LogInfoMsg("service is stopping")
                break

            src = os.path.join(source_dir, "VulnService_scripts.vbs")                      # MODIFY ME
            # copy contents of the source file to the destination preserving permissions
            shutil.copy(src, self.vbs)
            subprocess.call("cscript.exe %s" % self.vbs, shell=False)
            os.unlink(self.vbs)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Host your service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(VulnSvc)
        # Starts the service by calling the WIN32 'StartServiceCtrlDispatcher' function
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(VulnSvc)

