# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:34:30 2019

@author: eHonnef

Simple clicker, useful for afk botting while you can use another application in your computer.
This file is only for windows.
See requirements.txt
"""

import win32gui
import win32con
import win32api
import win32process
import win32ui
from time import sleep
from argparse import ArgumentParser
from sys import argv, exit


# Putting inside a class to change the variables values.
# Could be a better written class, but oh well
class Afk_Clicker:

  def __init__(self, mouse_btn=0, keyboard_key=0x0):
    self.mouse_btn = 0
    self.mouse_btn_up = 0
    self.mouse_btn_dn = 0

    self.keyboard_key = keyboard_key

    if (mouse_btn == 2):
      self.mouse_btn = win32con.MK_RBUTTON
      self.mouse_btn_up = win32con.WM_RBUTTONUP
      self.mouse_btn_dn = win32con.WM_RBUTTONDOWN
    elif (mouse_btn == 1):
      self.mouse_btn = win32con.MK_LBUTTON
      self.mouse_btn_up = win32con.WM_LBUTTONUP
      self.mouse_btn_dn = win32con.WM_LBUTTONDOWN

  # Get the window handler by its PID (using process name is not good).
  def get_hwnds_by_pid(self, pid):

    def callback(hwnd, hwnds):
      if (win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd)):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
          hwnds.append(hwnd)
      return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

  def get_hwnds_by_name(self, name):
    hwnd = win32gui.FindWindow(None, name)
    if (hwnd == None or hwnd == 0):
      hwnd = win32gui.FindWindow(name, None)

    return hwnd

  # This returns the sub/child handler
  def get_child_hwnd(self, hwnd):
    return win32gui.GetWindow(hwnd, win32con.GW_CHILD)

  # Creating the mouse click function (right button)
  # WM_LBUTTONDOWN and WM_LBUTTONUP is for left click.
  # You can check more in the link https://docs.microsoft.com/en-us/windows/desktop/inputdev/mouse-input-notifications
  def mouse_click(self, pycwnd):
    x = 300
    y = 300
    lParam = y << 15 | x
    pycwnd.SendMessage(self.mouse_btn_dn, self.mouse_btn, lParam)
    pycwnd.SendMessage(self.mouse_btn_up, 0, lParam)
    pycwnd.UpdateWindow()

  # Do a keystroke in the handler.
  # Change the hexadecimal value to the key you want.
  # Windows virtual keys: https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
  def keystroke(self, hwnd):
    win32api.PostMessage(
        self.get_child_hwnd(hwnd), win32con.WM_CHAR, self.keyboard_key, 0)

  # Create a "subwindow" from the handler. More info http://timgolden.me.uk/pywin32-docs/PyCWnd.html
  def make_pycwnd(self, hwnd):
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

  def run(self, hwndMain):
    if (hwndMain == 0 or hwndMain == None):
      raise Exception("Invalid handler, please check PID or process name")

    # Creating the "subwindow"
    pycwnd = self.make_pycwnd(hwndMain)
    while (True):
      # Simulating a mouse click
      if (self.mouse_btn != 0):
        self.mouse_click(pycwnd)
      # Simulating a keyboard keystroke
      if (self.keyboard_key != 0):
        self.keystroke(hwndMain)

      #sleep(1) this waits 1 second before looping through again
      sleep(1)


# Main execution code
def Main():
  # Initializing the argument line parser
  parser = ArgumentParser()

  # Mouse stuff
  parser.add_argument(
      "-m",
      "--mouse",
      type=int,
      help="0 or empty disable, 1 for left mouse click, 2 for right mouse click."
  )

  # Keyboard key
  parser.add_argument(
      "-k", "--key", help="Hexadecimal value for keyboard input. 0 disable.")

  # Obligatory (one or another)
  group = parser.add_mutually_exclusive_group()

  # Use process PID
  group.add_argument(
      "-p", "--pid", type=int, help="Target program PID, must be an integer")

  # Use process name
  group.add_argument("-n", "--name", help="Target program name")

  # If no argument was given, exit.
  if (len(argv) == 1):
    parser.print_help()
    exit(1)

  args = parser.parse_args()

  if (args.key == None):
    args.key = 0x0

  # Initialize class
  afk_Clicker = Afk_Clicker(args.mouse, args.key)

  # Getting handlers and running main code loop
  if (args.name != None):
    afk_Clicker.run(afk_Clicker.get_hwnds_by_name(args.name))
  elif (args.pid != None):
    afk_Clicker.run(afk_Clicker.get_hwnds_by_pid(args.pid)[0])

  parser.print_help()
  exit(1)


Main()
