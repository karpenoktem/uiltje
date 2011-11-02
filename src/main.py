import os
import wx
import sys
import time
import logging
import os.path
import threading
import subprocess

from utils import static_path, var_path, onWindows, subprocess_sui
from openvpn import OpenVPNConnection

IP_PHASSA = '10.18.0.1'

MENU_TOGGLE = wx.NewId()
MENU_FILES = wx.NewId()

STATE_UNKNOWN = 0
STATE_CONNECTED = 1
STATE_DISCONNECTED = 2

l = logging.getLogger(__name__)

class Icon(wx.TaskBarIcon):
    def __init__(self, program):
        super(Icon, self).__init__()
        self.icon_state_map = {
            STATE_CONNECTED: wx.Icon(static_path('enabled.png'),
                                     wx.BITMAP_TYPE_PNG),
            STATE_UNKNOWN: wx.Icon(static_path('unknown.png'),
                                   wx.BITMAP_TYPE_PNG),
            STATE_DISCONNECTED: wx.Icon(static_path('disabled.png'),
                                        wx.BITMAP_TYPE_PNG) }
        self.create_menu()
        self.program = program
    def set_state(self, state):
        self.SetIcon(self.icon_state_map[state], 'Uiltje')
        if state == STATE_CONNECTED:
            self.conn_toggle.Enable(True)
            self.conn_toggle.SetText('Verbreek &verbinding')
        elif state == STATE_DISCONNECTED:
            self.conn_toggle.Enable(True)
            self.conn_toggle.SetText('Maak &verbinding')
        elif state == STATE_UNKNOWN:
            self.conn_toggle.Enable(False)
            self.conn_toggle.SetText('Maak/verbreek &verbinding')
    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_left_up)
        self.menu = wx.Menu()
        self.menu.Append(MENU_FILES, "Naar &bestanden...")
        self.conn_toggle = self.menu.Append(MENU_TOGGLE, " ")
        self.menu.Append(wx.ID_EXIT, "&Afsluiten")
        self.menu.Bind(wx.EVT_MENU, self.on_menu_exit, id=wx.ID_EXIT)
        self.menu.Bind(wx.EVT_MENU, self.on_menu_files, id=MENU_FILES)
        self.menu.Bind(wx.EVT_MENU, self.on_menu_toggle, id=MENU_TOGGLE)
    def on_right_up(self, event):
        self.PopupMenu(self.menu)
    def on_left_up(self, event):
        self.program.show_files()
    def on_menu_files(self, event):
        self.program.show_files()
    def on_menu_exit(self, event):
        self.RemoveIcon()
        self.program.on_exit()
    def on_menu_toggle(self, event):
        self.program.toggle_connection()

class Program(object):
    def __init__(self):
        self.open_files_on_connection = False
        self.quiting = False
        self.exit_event = threading.Event()
    def set_state(self, state):
        self.state = state
        if not self.quiting:
            self.icon.set_state(state)
    def on_openvpn_connected(self):
        if onWindows:
            # For unknown reason, it can take quite some time before
            # "explorer \\10.18.0.1" works properly after connecting.
            # We poll using "net view \\10.18.0.1" until we're connected.
            # TODO is there a way to speed this up?
            while True:
                l.info("calling 'net view'")
                # WTF subprocess.Popen behaves differently than
                # subprocess.call.  This difference only occurs with
                # the custom startupinfo.
                pipe = subprocess.Popen(['net', 'view', '\\\\' + IP_PHASSA],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        startupinfo=subprocess_sui)
                out, code = pipe.communicate()
                # WTF in some instances code != pipe.returncode.  Is this
                # a bug of Python?
                if pipe.returncode == 0:
                    break
                l.debug("returncode: %s", pipe.returncode)
                time.sleep(0.5)
                if self.quiting:
                    return
        self.set_state(STATE_CONNECTED)
        if self.open_files_on_connection:
            self._show_files()
            self.open_files_on_connection = False
    def _vpn_worker_entry(self):
        self.set_state(STATE_UNKNOWN)
        self.vpnconn.run()
        self.set_state(STATE_DISCONNECTED)
    def on_exit(self):
        self.quiting = True
        if self.state != STATE_DISCONNECTED:
            self.set_state(STATE_UNKNOWN)
            self.vpnconn.stop()
        self.app.ExitMainLoop()
        self.exit_event.set()
    def connect(self):
        assert self.state == STATE_DISCONNECTED
        self.vpn_worker = threading.Thread(target=self._vpn_worker_entry)
        self.vpn_worker.start()
    def main(self):
        self.app = wx.App()
        self.vpnconn = OpenVPNConnection(self.on_openvpn_connected)
        self.icon = Icon(self)
        self.set_state(STATE_DISCONNECTED)
        self.connect()
        self.app.MainLoop()
        self.exit_event.wait()
        sys.exit()
    def show_files(self):
        if self.state == STATE_CONNECTED:
            self._show_files()
        else:
            self.open_files_on_connection = True
            if self.state == STATE_DISCONNECTED:
                self.connect()
    def _show_files(self):
        if onWindows:
            l.info("calling explorer")
            # WTF adding startupinfo breaks this.
            subprocess.call(['explorer', '\\\\' + IP_PHASSA])
        # TODO implement for other platforms
    def toggle_connection(self):
        if self.state == STATE_CONNECTED:
            self.set_state(STATE_UNKNOWN)
            self.vpnconn.stop()
        elif self.state == STATE_DISCONNECTED:
            self.connect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fileHandler = logging.FileHandler(var_path('log.txt'), mode='a')
    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s")
    fileHandler.setFormatter(formatter)
    logging.root.addHandler(fileHandler)
    Program().main()
