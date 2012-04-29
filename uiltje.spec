# -*- mode: python -*-

import os
import os.path

datas = []
def datas_dir(trgDir, srcDir):
	ret = []
	s = [(srcDir, trgDir)]
	while s:
		cSrcDir, cTrgDir = s.pop()
		for child in os.listdir(cSrcDir):
			childSrcPath = os.path.join(cSrcDir, child)
			childTrgPath = os.path.join(cTrgDir, child)
			if os.path.isfile(childSrcPath):
				ret.append((childTrgPath, childSrcPath, 'DATA'))
			elif os.path.isdir(childSrcPath):
				s.append((childSrcPath, childTrgPath))
	return ret
datas += datas_dir('static', 'static')

a = Analysis(['src/main.py'],
             pathex=['C:\\Documents and Settings\\John Doo\\My Documents\\uiltje'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\main', 'uiltje.exe'),
          debug=False,
          strip=None,
          upx=True,
		  icon="uiltje.ico",
          console=False )

datas += a.datas

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'main'))
