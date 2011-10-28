import os
import wx
import os
import sys
import os.path
import subprocess

MENU_CONNECT = wx.NewId()
MENU_FILES = wx.NewId()

from utils import data_path

class Icon(wx.TaskBarIcon):
    def __init__(self, program):
        super(Icon, self).__init__()
        self.SetIcon(wx.Icon(data_path('kn.ico'), wx.BITMAP_TYPE_ICO),
                                                 "KNTray")
        self.create_menu()
        self.program = program
    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.on_right_up)
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_left_up)
        self.menu = wx.Menu()
        self.menu.Append(MENU_FILES, "Naar &bestanden...")
        self.menu.Append(MENU_CONNECT, "&Verbinden")
        self.menu.Append(wx.ID_EXIT, "&Afsluiten")
        self.menu.Bind(wx.EVT_MENU, self.on_menu_exit, id=wx.ID_EXIT)
        self.menu.Bind(wx.EVT_MENU, self.on_menu_files, id=MENU_FILES)
    def on_right_up(self, event):
        self.PopupMenu(self.menu)
    def on_left_up(self, event):
        self.program.show_files()
    def on_menu_files(self, event):
        self.program.show_files()
    def on_menu_exit(self, event):
        self.RemoveIcon()
        self.program.on_exit()

class Program(object):
    def __init__(self):
        import threading
        from openvpn import run_openvpn
        threading.Thread(target=run_openvpn).start()
    def on_exit(self):
        self.app.ExitMainLoop()
    def main(self):
        self.app = wx.App()
        self.icon = Icon(self)
        self.app.MainLoop()
    def show_files(self):
        subprocess.call(['explorer', '\\\\10.18.0.1'])

if __name__ == '__main__':
    Program().main()
