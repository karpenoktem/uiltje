import logging
import subprocess
from utils import onWindows, data_path, subprocess_sui

if onWindows:
    from win_tap import ensure_tap_installed

l = logging.getLogger(__name__)

def run_openvpn():
    if onWindows:
        ensure_tap_installed()
    p = subprocess.Popen([data_path('openvpn/openvpn'), '--config', 'user.ovpn'],
                         cwd=data_path('user'),
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         startupinfo=subprocess_sui)
    while True:
        line = p.stdout.readline()
        if line == '':
            break
        line = line.strip()
        l.debug(line)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    p = run_openvpn()
