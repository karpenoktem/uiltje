import logging
import subprocess
from utils import static_path, subprocess_sui

TAP_NAME = 'tap0901'

l = logging.getLogger(__name__)

def _get_tap_status():
    return subprocess.check_output([static_path('tap/tapinstall'), 'status',
                                    '*%s*' % TAP_NAME],
                                    startupinfo=subprocess_sui)

def ensure_tap_installed():
    # XXX Does this work on non-english Windows?
    if 'No matching devices found' in _get_tap_status():
        l.info('No tap device found -- installing')
        install_tap()
    else:
        l.info('tap device found -- do not install our own')

def install_tap():
    subprocess.call([static_path('tap/tapinstall'), 'install',
                     static_path('tap/OemWin2k.inf'), TAP_NAME],
                                     startupinfo=subprocess_sui)

def remove_tap():
    # Only remove tap if there is a single tap running.
    # XXX Does this work on non-english Windows?
    if '1 matching device(s) found.' in _get_tap_status():
        l.info('removing single tap device')
        subprocess.call([static_path('tap/tapinstall'), 'remove', TAP_NAME],
                                     startupinfo=subprocess_sui)
    else:
        l.info('several tap devices found - not removing any of them')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ensure_tap_installed()
