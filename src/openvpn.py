import logging
import threading
import subprocess
from utils import onWindows, var_path, static_path, subprocess_sui

if onWindows:
    from win_tap import ensure_tap_installed

l = logging.getLogger(__name__)

class OpenVPNConnection(object):
    def __init__(self, on_connected=None):
        self.on_connected = on_connected
        self.p = None
    def run(self):
        if onWindows:
            ensure_tap_installed()
        self.p = subprocess.Popen([static_path('openvpn/openvpn'),
                                   '--config', 'user.ovpn'],
                             cwd=var_path('user'),
                             stdout=subprocess.PIPE,
                             startupinfo=subprocess_sui)
        while True:
            line = self.p.stdout.readline()
            if line == '':
                break
            line = line.strip()
            if "Initialization Sequence Completed" in line:
                if self.on_connected:
                    self.on_connected()
            l.debug(line)
        # XXX Should we remove the TAP device after use?
    def stop(self):
        if self.p:
            self.p.kill()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    OpenVPNConnection().run()
