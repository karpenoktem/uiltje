from base64 import b64encode
from cStringIO import StringIO

import os
import os.path
import urllib2
import zipfile
import logging

l = logging.getLogger(__name__)

from utils import var_path
from common import *

class AuthFailed(Exception):
    pass

def _download(username, password):
    req = urllib2.Request(CERT_DOWNLOAD_URI % username)
    req.add_header("Authorization",
                       "Basic %s" % b64encode("%s:%s" % (username, password)))
    try:
        fh = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        if e.code == 401:
            raise AuthFailed
        raise e
    return StringIO(fh.read())

def _extract_zip(f):
    def extract(zipf, sn, td, tn):
        with zipf.open(sn) as fi:
            with open(os.path.join(td, tn), 'w') as fo:
                while True:
                    buf = fi.read(4096)
                    if not buf:
                        break
                    fo.write(buf)
    if not os.path.exists(var_path('user')):
        os.mkdir(var_path('user'), 0700)
    with zipfile.ZipFile(f, 'r') as zipf:
        for fn in zipf.namelist():
            if fn.endswith('.ovpn'):
                extract(zipf, fn, var_path('user'), 'user.ovpn')
            elif fn.endswith('ca.crt'):
                extract(zipf, fn, var_path('user'), 'ca.crt')
            elif fn.endswith('.crt'):
                extract(zipf, fn, var_path('user'), os.path.basename(fn))
            elif fn.endswith('.key'):
                extract(zipf, fn, var_path('user'), os.path.basename(fn))
            else:
                l.info('Stray file %s in zip', fn)

def fetch(username, password):
    _extract_zip(_download(username, password))
