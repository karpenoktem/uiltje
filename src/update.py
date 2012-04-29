from urllib2 import Request, urlopen, HTTPError
import os
from zipfile import ZipFile
from cStringIO import StringIO

from utils import var_path, onWindows, base_path, escapeshellarg

class BaseUpdater:
	def __init__(self):
		self.deletes = set()
		self.updates = set()

	def delete_file(self, fn):
		self.deletes.add(fn)

	def update_file(self, fn, new_file):
		self.updates.add((fn, new_file))

	def clean_deletes(self):
		for fn, new_file in self.updates:
			try:
				self.deletes.remove(fn)
			except:
				pass
			try:
				self.deletes.remove(new_file)
			except:
				pass

	def precreate_dirs(self):
		for fn, new_file in self.updates:
			if not os.path.exists(os.path.dirname(fn)):
				os.makedirs(os.path.dirname(fn))

class WindowsUpdater(BaseUpdater):
	def commit(self, etag):
		self.clean_deletes()
		self.precreate_dirs()
		batch_file = base_path("update.bat")
		with open(batch_file, 'w') as fh:
			fh.write("ping -n 5 127.0.0.1 >nul\r\n")
			for fn, new_file in self.updates:
				fh.write('move %s %s\r\n' % (escapeshellarg(base_path(new_file)), escapeshellarg(base_path(fn))))
			for fn in self.deletes:
				fh.write('del %s\r\n' % escapeshellarg(base_path(fn)))
			fh.write('echo -n %s > %s\n' % (etag, escapeshellarg(base_path('etag.dat'))))
			fh.write('del %s\r\n' % escapeshellarg(batch_file))
			fh.write('rmdir /s /q %s\r\n' % escapeshellarg(batch_file))
			fh.write(escapeshellarg(base_path('uiltje.exe')))
		subprocess.call([batch_file])
		sys.exit(0)

class UnixUpdater(BaseUpdater):
	def commit(self, etag):
		self.clean_deletes()
		self.precreate_dirs()
		batch_file = base_path("update.sh")
		with open(batch_file, 'w') as fh:
			fh.write("sleep 5\n")
			for fn, new_file in self.updates:
				fh.write('mv %s %s\n' % (escapeshellarg(base_path(new_file)), escapeshellarg(base_path(fn))))
			for fn in self.deletes:
				fn = base_path(fn)
				if os.path.isdir(fn):
					fh.write('rmdir %s\n' % escapeshellarg(fn))
				else:
					fh.write('rm %s\n' % escapeshellarg(fn))
			fh.write('echo -n %s > %s\n' % (etag, escapeshellarg(base_path('etag.dat'))))
			fh.write('rm -r %s\n' % escapeshellarg(base_path('update')))
			fh.write('rm %s\n' % escapeshellarg(batch_file))
			fh.write(escapeshellarg(base_path('uiltje.exe')))

def get_current_etag():
	path = base_path('etag.dat')
	try:
		with open(path, 'r') as fh:
			etag = fh.read()
	except:
		return None
	return etag

def update():
	etag = get_current_etag()
	# req = Request('http://www.karpenoktem.nl/smoelen/uiltje-files.zip')
	# req = Request('https://github.com/karpenoktem/uiltje/zipball/master')
	req = Request('http://kn.cx/groups/webcie/uiltje/Uiltje%20beta%201.zip')
	if etag is not None:
		req.add_header("If-None-Match", etag)
	try:
		fh = urlopen(req)
	except HTTPError as e:
		if e.code == 304:
			return False
		raise
# XXX uncommenten
#	if fh.info()['ETag'] == etag:
#		return False
#	etag = fh.info()['ETag']
	print fh.info()
	etag = "piet"
	zipdata = StringIO(fh.read())
	if onWindows:
		updater = WindowsUpdater()
	else:
		updater = UnixUpdater()
	q = [base_path('')]
	while q:
		cur = q.pop()
		for fn in os.listdir(cur):
			fp = os.path.join(cur, fn)
			if os.path.isdir(fp):
				q.append(fp)
			else:
				updater.delete_file(fp)
	zipf = ZipFile(zipdata, 'r')
	zipf.extractall(base_path('update'))
	for fn in zipf.namelist():
		if not os.path.isdir(base_path(os.path.join('update', fn))):
			updater.update_file(fn, base_path(os.path.join('update', fn)))
	updater.commit(etag)

if __name__ == '__main__':
	print update()
