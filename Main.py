# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:34:30 2019

@author: eHonnef

Simple clicker, useful for afk botting while you can use another application in your computer.
Only available for windows.
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


# Get the window handler by its PID (using process name is not good).
def get_hwnds_by_pid(pid):

  def callback(hwnd, hwnds):
    if (win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd)):
      _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
      if found_pid == pid:
        hwnds.append(hwnd)
    return True

  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds


def get_hwnds_by_name(name):
  hwnd = win32gui.FindWindow(None, name)
  if (hwnd == None or hwnd == 0):
    hwnd = win32gui.FindWindow(name, None)

  return hwnd


# This returns the sub/child handler
def get_child_hwnd(hwnd):
  return win32gui.GetWindow(hwnd, win32con.GW_CHILD)


# Creating the mouse click function (right button)
# WM_LBUTTONDOWN and WM_LBUTTONUP is for left click.
# You can check more in the link https://docs.microsoft.com/en-us/windows/desktop/inputdev/mouse-input-notifications
def mouse_click(pycwnd):
  x = 300
  y = 300
  lParam = y << 15 | x
  pycwnd.SendMessage(win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
  pycwnd.SendMessage(win32con.WM_RBUTTONUP, 0, lParam)
  pycwnd.UpdateWindow()


# Do a keystroke in the handler.
# Change the hexadecimal value to the key you want.
# Windows virtual keys: https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
def keystroke(hwnd):
  win32api.PostMessage(get_child_hwnd(hwnd), win32con.WM_CHAR, 0x44, 0)


# Create a "subwindow" from the handler. More info http://timgolden.me.uk/pywin32-docs/PyCWnd.html
def make_pycwnd(hwnd):
  PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
  return PyCWnd


def run(hwndMain):
  if (hwndMain == 0 or hwndMain == None):
    raise Exception("Invalid handler, please check PID or process name")

  # Creating the "subwindow"
  pycwnd = make_pycwnd(hwndMain)
  while (True):
    # Simulating a mouse click
    mouse_click(pycwnd)
    # Simulating a keyboard keystroke
    keystroke(hwndMain)

    #sleep(1) this waits 1 second before looping through again
    sleep(1)


# Main execution code
def Main():
  parser = ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument(
      "-p",
      "--pid",
      dest="pid",
      type=int,
      help="Target program PID, must be an integer")
  group.add_argument("-n", "--name", dest="name", help="Target program name")

  if (len(argv) == 1):
    parser.print_help()
    exit(1)

  args = parser.parse_args()
  if (args.name != None):
    run(get_hwnds_by_name(args.name))
  elif (args.pid != None):
    run(get_hwnds_by_pid(args.pid)[0])


Main()
