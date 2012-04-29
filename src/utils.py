import os
import sys
import os.path
import platform
import subprocess

def base_path(pth):
    if not onWindows:
        return os.path.abspath(os.path.join(os.getcwd(), '..', pth))
    # Normal case
    if not sys.executable.endswith('pythonw.exe'):
        return os.path.abspath(os.path.join(os.path.dirname(sys.executable),
                            pth))
    # For debugging
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..',
                        pth))

def var_path(pth):
    if not onWindows:
        return os.path.abspath(os.path.join(os.getenv('HOME'), '.uiltje', pth))
    return base_path(os.path.join('var', pth))

def static_path(pth):
    return base_path(os.path.join('static', pth))

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

def escapeshellarg(s):
    return "'" + s.replace("'", "'\\''") + "'"

onWindows = platform.system() == 'Windows'

# for windowless subprocess(.)calls
subprocess_sui = None
if onWindows:
    subprocess_sui = subprocess.STARTUPINFO()
    subprocess_sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
