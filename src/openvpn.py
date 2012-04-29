import logging
import threading
import subprocess
from utils import onWindows, var_path, static_path, subprocess_sui

if onWindows:
    from win_tap import ensure_tap_installed, remove_tap

l = logging.getLogger(__name__)

class OpenVPNConnection(object):
    def __init__(self, on_connected=None):
        self.on_connected = on_connected
        self.p = None
    def run(self):
        if onWindows:
            ensure_tap_installed()
            executable = static_path('openvpn/openvpn')
        else:
            executable = 'openvpn'
        self.p = subprocess.Popen([executable,
                                   '--config', 'user.ovpn'],
                             cwd=var_path('user'),
                             stdout=subprocess.PIPE,
                             startupinfo=subprocess_sui)
        while True:
            line = self.p.stdout.readline()
            if line == '':
                break
            line = line.strip()
            l.debug(line)
            if "Initialization Sequence Completed" in line:
                if self.on_connected:
                    self.on_connected()
    def stop(self):
        if self.p:
            self.p.kill()
        if onWindows:
            remove_tap()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    OpenVPNConnection().run()
