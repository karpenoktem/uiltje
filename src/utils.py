import os
import sys
import os.path
import platform
import subprocess

def data_path(pth):
    # TODO addapt for installation
    return os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),
                        'data', pth)

onWindows = platform.system() == 'Windows'

# for windowless subprocess(.)calls
subprocess_sui = None
if onWindows:
    subprocess_sui = subprocess.STARTUPINFO()
    subprocess_sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
