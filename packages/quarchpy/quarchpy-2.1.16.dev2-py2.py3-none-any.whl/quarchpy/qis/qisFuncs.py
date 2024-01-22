"""
Contains general functions for starting and stopping QIS processes
"""

import os, sys 
import time, platform 
from quarchpy.connection_specific.connection_QIS import QisInterface
from quarchpy.user_interface.user_interface import printText
import subprocess
import logging

def isQisRunning(): 
    """
    Checks if a local instance of QIS is running and responding
    
    Returns
    -------
    is_running : bool
        True if QIS is running and responding

    """
 
    qisRunning = False
    myQis = None
    
    #attempt to connect to Qis
    try:
        myQis = QisInterface(connectionMessage=False)
        if (myQis is not None):
            #if we can connect to qis, it's running
            qisRunning = True 
    except:
        #if there's no connection to qis, an exception will be caught
        pass    
     
    if (qisRunning is False):
        logging.debug("QIS is not running")
        return False 
    else:
        logging.debug("QIS is running")
        return True
 
def startLocalQis(terminal=False, headless=False, args=None):
    """
    Executes QIS on the local system, using the version contained within quarchpy
    
    Parameters
    ----------
    terminal : bool, optional
        True if QIS terminal should be shown on startup
    headless : bool, optional
        True if app should be run in headless mode for non graphical environments
    args : list[str], optional
        List of additional parameters to be supplied to QIS on the command line

    """

    # java path
    java_path = os.path.dirname(os.path.abspath(__file__))
    java_path, junk = os.path.split(java_path)
    java_path = os.path.join(java_path, "connection_specific", "jdk-j21-jres")

    # change directory to /QPS/QIS
    qis_path = os.path.dirname(os.path.abspath(__file__))
    qis_path,junk = os.path.split (qis_path)

    # OS
    current_os = platform.system()

    # ensure the jres folder has the required permissions
    if current_os != "Windows":
        subprocess.call(['chmod', '-R', '+rwx', java_path])

    # single or multiple QPS builds for each OS
    is_single_qps_build = True
    if is_single_qps_build:
        qis_path = os.path.join(qis_path, "connection_specific", "QPS", "win-amd64", "qis", "qis.jar")
    else:
        if current_os in "Windows":
            qis_path = os.path.join(qis_path, "connection_specific", "QPS", "win-amd64", "qis", "qis.jar")
        elif current_os in "Linux":
            qis_path = os.path.join(qis_path, "connection_specific", "QPS", "lin-amd64", "qis", "qis.jar")
        elif current_os in "Darwin":
            qis_path = os.path.join(qis_path, "connection_specific", "QPS", "mac-amd64", "qis", "qis.jar")
        else:  # default to windows
            qis_path = os.path.join(qis_path, "connection_specific", "QPS", "win-amd64", "qis", "qis.jar")

    os.chdir(os.path.dirname(qis_path))

    # Building the command
    # Process command prefix. Needed for headless mode, to support OSs with no system tray.
    if headless is True or (args is not None and "-headless" in args):
        cmd_prefix = "java -Djava.awt.headless=true"
    else:
        cmd_prefix = "java"
    # Process command suffix (additional standard options for QIS).
    if terminal is True:
        cmd_suffix = " -terminal"
    else:
        cmd_suffix = ""
    if args is not None:
        for option in args:
            # Avoid doubling the terminal option
            if option == "-terminal" and terminal is True:
                continue
            # Headless option is processed seperately as a java command
            if option != "-headless":
                cmd_suffix = cmd_suffix + " " + option

    # record current working directory
    current_dir = os.getcwd()

    command = cmd_prefix + " -jar qis.jar" + cmd_suffix
    
    # different start for different OS
    if current_os == "Windows":
        command = java_path + "\\win-amd64-jdk-21-jre\\bin\\" + command
    elif current_os == "Linux":
        command = java_path + "/lin-amd64-jdk-21-jre/bin/" + command
    elif current_os == "Darwin":
        command = java_path + "/mac-amd64-jdk-21-jre/bin/" + command
    else:  # default to windows
        command = java_path + "\\win-amd64-jdk-21-jre\\bin\\" + command

    # Use the command and check QIS has launched
    if "-logging=ON" in str(args): #If logging to a terminal window is on then os.system should be used to view logging.
        os.system(command)
    else:
        if sys.version_info[0] < 3:
            sp=os.popen2(command + " 2>&1")
        else:
            sp=os.popen(command + " 2>&1")
        startTime = time.time() #Checks for Popen launch only
        timeout = 10
        while not isQisRunning():
            if time.time() - startTime > timeout:
                raise TimeoutError("QIS failed to launch within timelimit of " + str(timeout) + " sec.")
            time.sleep(0.2)
            pass
    
    # change directory back to start directory
    os.chdir(current_dir)


def check_remote_qis(host='127.0.0.1', port=9722, timeout=0):
    """
        Checks if a local or specified instance of QIS is running and responding
        This continues to scan until qis is found or a timeout is hit.

        Returns
        -------
        is_running : bool
            True if QIS is running and responding

        """

    qisRunning = False
    myQis = None

    start = time.time()
    while True:
        # attempt to connect to Qis
        try:
            myQis = QisInterface(host=host, port=port, connectionMessage=False)
            if (myQis is not None):
                # if we can connect to qis, it's running
                qisRunning = True
                break
        except:
            # if there's no connection to qis, an exception will be caught
            pass
        if (time.time() - start) > timeout:
            break

    if (qisRunning is False):
        logging.debug("QIS is not running")
        return False
    else:
        logging.debug("QIS is running")
        return True

def checkAndCloseQis(host='127.0.0.1', port=9722):
    if isQisRunning() is True:
        closeQis()


def closeQis(host='127.0.0.1', port=9722):
    """
    Helper function to close an instance of QIS.  By default this is the local version, but
    an address can be specified for remote systems.
    
    Parameters
    ----------
    host : str, optional
        Host IP address if not localhost
    port : str, optional
        QIS connection port if set to a value other than the default
        
    """
    
    myQis = QisInterface(host, port)
    retVal=myQis.sendAndReceiveCmd(cmd = "$shutdown")
    myQis.disconnect()
    time.sleep(1)
    return retVal

#DEPRICATED
def GetQisModuleSelection (QisConnection):
    """
    Prints a list of modules for user selection
    
    .. deprecated:: 2.0.12
        Use the module selection functions of the QisInterface class instead
    """
    
    # Request a list of all USB and LAN accessible power modules
    devList = QisConnection.getDeviceList()
    # Removes rest devices
    devList = [ x for x in devList if "rest" not in x ]

    # Print the devices, so the user can choose one to connect to
    printText ("\n ########## STEP 1 - Select a Quarch Module. ########## \n")
    printText (' --------------------------------------------')
    printText (' |  {:^5}  |  {:^30}|'.format("INDEX", "MODULE"))
    printText (' --------------------------------------------')
        
    try:
        for idx in xrange(len(devList)):
            printText (' |  {:^5}  |  {:^30}|'.format(str(idx+1), devList[idx]))
            printText(' --------------------------------------------')
    except:
        for idx in range(len(devList)):
            printText (' |  {:^5}  |  {:^30}|'.format(str(idx+1), devList[idx]))
            printText(' --------------------------------------------')

    # Get the user to select the device to control
    try:
        moduleId = int(raw_input ("\n>>> Enter the index of the Quarch module: "))
    except NameError:
        moduleId = int(input ("\n>>> Enter the index of the Quarch module: "))

    # Verify the selection
    if (moduleId > 0 and moduleId <= len(devList)):
        myDeviceID = devList[moduleId-1]
    else:
        myDeviceID = None

    return myDeviceID
 
 
