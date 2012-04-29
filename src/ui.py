import os
import wx
import logging

from utils import static_path
from common import *

MENU_TOGGLE = wx.NewId()
MENU_FILES = wx.NewId()

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
