import os
import sys
import os.path
import platform
import subprocess

def var_path(pth):
    if not onWindows:
        return os.path.abspath(os.path.join(os.getenv('HOME'), '.uiltje', pth))
    # Normal case
    if not sys.executable.endswith('pythonw.exe'):
        return os.path.abspath(os.path.join(os.path.dirname(sys.executable),
                            'var', pth))
    # For debugging
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..',
                        'var', pth))

def static_path(pth):
    if not onWindows:
        return os.path.abspath(os.path.join(os.getcwd(), '..', 'static', pth))
    # Normal case
    if not sys.executable.endswith('pythonw.exe'):
        return os.path.join(os.path.abspath(os.path.dirname(sys.executable)),
                            'static', pth)
    # For debugging
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..',
                        'static', pth))

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

onWindows = platform.system() == 'Windows'

# for windowless subprocess(.)calls
subprocess_sui = None
if onWindows:
    subprocess_sui = subprocess.STARTUPINFO()
    subprocess_sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
