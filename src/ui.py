import os
import wx
import logging

from utils import static_path
from common import *

MENU_TOGGLE = wx.NewId()
MENU_FILES = wx.NewId()

l = logging.getLogger(__name__)

class LoginDialog(wx.Dialog):
    def __init__(self, callback, message=None):
        super(LoginDialog, self).__init__(None,
                                          title="Uiltje login")
        # Create controls
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        loginButton = wx.Button(self, label='Login')
        loginButton.Bind(wx.EVT_BUTTON, self.on_login)
        cancelButton = wx.Button(self, label='Cancel')
        cancelButton.Bind(wx.EVT_BUTTON, self.on_cancel)
        loginButton.SetDefault()
        userName_l = wx.StaticText(panel, wx.ID_ANY, 'Gebruikersnaam')
        password_l = wx.StaticText(panel, wx.ID_ANY, 'Wachtwoord')
        userName_tb = wx.TextCtrl(panel)
        password_tb = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        grid.Add(userName_l)
        grid.Add(userName_tb)
        grid.Add(password_l)
        grid.Add(password_tb)
        panel.SetSizer(grid)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(loginButton)
        hbox.Add(cancelButton, flag=wx.LEFT, border=5)
        vbox.Add(panel, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        if message:
            msg_l = wx.StaticText(self, wx.ID_ANY, message)
            vbox.Add(msg_l, flag=wx.ALIGN_CENTER, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.SetSizerAndFit(vbox)

        # Store
        self.callback = callback
        self.userName_tb = userName_tb
        self.password_tb = password_tb

        # Show!
        self.ShowModal()
    def on_login(self, e):
        creds = (self.userName_tb.GetValue(),
                 self.password_tb.GetValue())
        self.Destroy()
        self.callback(creds)
    def on_cancel(self, e):
        self.Destroy()
        self.callback(None)

class Icon(wx.TaskBarIcon):
    def __init__(self, program):
        super(Icon, self).__init__()
        self.icon_state_map = {
            STATE_CONNECTED: wx.Icon(static_path('enabled.png'),
                                     wx.BITMAP_TYPE_PNG),
            STATE_DISCONNECTED: wx.Icon(static_path('disabled.png'),
                                        wx.BITMAP_TYPE_PNG),
            None: wx.Icon(static_path('unknown.png'),
                                   wx.BITMAP_TYPE_PNG) }
        self.create_menu()
        self.program = program
    def set_state(self, state):
        self.SetIcon(self.icon_state_map.get(state,
                        self.icon_state_map[None]), 'Uiltje')
        if state == STATE_CONNECTED:
            self.conn_toggle.Enable(True)
            self.conn_toggle.SetText('Verbreek &verbinding')
        elif state == STATE_DISCONNECTED:
            self.conn_toggle.Enable(True)
            self.conn_toggle.SetText('Maak &verbinding')
        else:
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
