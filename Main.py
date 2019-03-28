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


# Get the window handler by its PID (using process name is not good).
def get_hwnds(pid):

  def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
      _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
      if found_pid == pid:
        hwnds.append(hwnd)
    return True

  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds


# This returns the sub/child handler
def getChildHwnd(hwnd):
  return win32gui.GetWindow(hwnd, win32con.GW_CHILD)


# Creating the mouse click function (right button)
# WM_LBUTTONDOWN and WM_LBUTTONUP is for left click.
# You can check more in the link https://docs.microsoft.com/en-us/windows/desktop/inputdev/mouse-input-notifications
def f_click(pycwnd):
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
  win32api.PostMessage(getChildHwnd(hwnd), win32con.WM_CHAR, 0x44, 0)


# Create a "subwindow" from the handler. More info http://timgolden.me.uk/pywin32-docs/PyCWnd.html
def make_pycwnd(hwnd):
  PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
  return PyCWnd


# Main execution code
def Main(pid):
  # Getting the handler
  hwndMain = get_hwnds(pid)[0]

  if (hwndMain == 0):
    raise Exception("Invalid handler")

  while (True):
    # Creating the "subwindow"
    pycwnd = make_pycwnd(hwndMain)
    # Simulating a mouse click
    f_click(pycwnd)
    # Simulating a keyboard keystroke
    keystroke(hwndMain)

    #sleep(1) this waits 1 second before looping through again
    sleep(1)


Main(10664)
