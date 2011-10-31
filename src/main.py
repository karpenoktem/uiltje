import os
import wx
import os
import sys
import logging
import os.path
import threading
import subprocess

from utils import data_path
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
            STATE_CONNECTED: wx.Icon(data_path('enabled.png'),
                                     wx.BITMAP_TYPE_PNG),
            STATE_UNKNOWN: wx.Icon(data_path('unknown.png'),
                                   wx.BITMAP_TYPE_PNG),
            STATE_DISCONNECTED: wx.Icon(data_path('disabled.png'),
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
        self.program.on_exit()
    def on_menu_toggle(self, event):
        self.program.toggle_connection()

class Program(object):
    def __init__(self):
        self.open_files_on_connection = False
    def set_state(self, state):
        self.state = state
        self.icon.set_state(state)
    def on_openvpn_connected(self):
        self.set_state(STATE_CONNECTED)
        if self.open_files_on_connection:
            self._show_files()
            self.open_files_on_connection = False
    def _vpn_worker_entry(self):
        self.set_state(STATE_UNKNOWN)
        self.vpnconn.run()
        self.set_state(STATE_DISCONNECTED)
    def on_exit(self):
        if self.state != STATE_DISCONNECTED:
            self.set_state(STATE_UNKNOWN)
            self.vpnconn.stop()
        self.app.ExitMainLoop()
        sys.exit()
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
    def show_files(self):
        if self.state == STATE_CONNECTED:
            self._show_files()
        else:
            self.open_files_on_connection = True
            if self.state == STATE_DISCONNECTED:
                self.connect()
    def _show_files(self):
        subprocess.call(['explorer', '\\\\' + IP_PHASSA])
    def toggle_connection(self):
        if self.state == STATE_CONNECTED:
            self.set_state(STATE_UNKNOWN)
            self.vpnconn.stop()
        elif self.state == STATE_DISCONNECTED:
            self.connect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Program().main()
