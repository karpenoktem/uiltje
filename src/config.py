from base64 import b64encode
from urllib2 import Request, urlopen, HTTPError

class AuthenticationFailed(Exception):
	pass

class InternalError(Exception):
	pass


def download(user, password):
	req = Request('https://www.karpenoktem.nl/smoelen/ik/openvpn/openvpn-config-%s.zip' % user)
	req.add_header("Authorization", "Basic %s" % b64encode("%s:%s" % (user, password)))
	try:
		fh = urlopen(req)
	except HTTPError as e:
		if e.code == 401:
			raise AuthenticationFailed
		else
			raise InternalError, e
	# XXX leest dit alles?
	return fh.read()

def extract_zip(user, password):
	# XXX move files to the right place
	zipdata = download(user, password)
	with ZipFile(zipdata, 'r') as zipf:
		for fn in zipf.namelist():
			# XXX

if __name__ == '__main__':
	print download('yourname', 'yourpass')
