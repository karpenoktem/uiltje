import logging
import subprocess
from utils import data_path, subprocess_sui

TAP_NAME = 'tap0901'

l = logging.getLogger(__name__)

def ensure_tap_installed():
    output = subprocess.check_output([data_path('tap/tapinstall'), 'status',
                                     '*%s*' % TAP_NAME],
                                     startupinfo=subprocess_sui)
    if 'No matching devices found' in output:
        l.info('No tap device found -- installing')
        install_tap()
    else:
        l.info('tap device found -- do not install our own')

def install_tap():
    subprocess.call([data_path('tap/tapinstall'), 'install',
                     data_path('tap/OemWin2k.inf'), TAP_NAME],
                                     startupinfo=subprocess_sui)

def remove_tap():
    subprocess.call([data_path('tap/tapinstall'), 'remove', TAP_NAME],
                                     startupinfo=subprocess_sui)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ensure_tap_installed()
