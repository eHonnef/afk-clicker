# AFK clicker

A simple AFK clicker that allow to simulate keystrokes (mouse or keyboard) even if the window isn't focused.

Tested using notepad and minecraft (afk fish farm :D).  
If you tested in another game/application please let me know opening an issue or even contribuiting making a pull request.  
For now it's only work on windows.

## Usage

Just take the application PID from the task manager and replace in the Main() function call.  
For minecraft users: press F3 + p to disable the pause menu when you change the focus (use windows key or atl + tab to change window).

## Requirements

Python 3 (tested with 3.7).  
For libraries check the file `requirements.txt` or run the command `pip install -r requirements.txt`.