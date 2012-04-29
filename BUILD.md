You will need

  * To run Uiltje from source:
    * Python 2
    * WxPython
    * These files in static/tap
       * OemWin2k.inf
       * tap0901.cat
       * tap0901.sys
       * tapinstall.exe
    * These files in openvpn
       * libeay32.dll
       * libssl32.dll
       * openvpn.exe
  * To create a EXE:
    * PyInstaller
    * UPX (optional)
  * To create the installer:
    * NSIS
    * NSIS Self-Extractor Kit

First, test Uiltje from source.  Run:

    path\to\python.exe main.py

Then create the stand-alone EXE:

    path\to\python.exe path\to\pyinstaller.py main.spec

pyinstaller will put the EXE in dist/main.  Test it.  Then right-click on
Uiltje.nsi and select "Compile NSI Script".  That's it.

