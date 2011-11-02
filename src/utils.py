import os
import sys
import os.path
import platform
import subprocess

def var_path(pth):
    # Normal case
    if not sys.executable.endswith('pythonw.exe'):
        return os.path.join(os.path.abspath(os.path.dirname(sys.executable)),
                            'var', pth)
    # For debugging
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..',
                        'var', pth))

def static_path(pth):
    # Normal case
    if not sys.executable.endswith('pythonw.exe'):
        return os.path.join(os.path.abspath(os.path.dirname(sys.executable)),
                            'static', pth)
    # For debugging
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..',
                        'static', pth))

onWindows = platform.system() == 'Windows'

# for windowless subprocess(.)calls
subprocess_sui = None
if onWindows:
    subprocess_sui = subprocess.STARTUPINFO()
    subprocess_sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
