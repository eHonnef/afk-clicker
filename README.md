# AFK clicker

A simple AFK clicker that allow to simulate keystrokes (mouse or keyboard) even if the window isn't focused.

Tested using notepad and minecraft (afk fish farm :D).  
If you tested in another game/application please let me know opening an issue or even contribuiting making a pull request.  
For now it only work on windows.

## Usage

Just take the application PID from the task manager and call as `python Main.py -p PID_NUMBER`.  
Or you can use the application name from task manager and call as `python Main.py -n "APPLICATION NAME"`, remember that applications can have more than one name, take minecraft for example, in task manager you see as `Java(TM) Platform SE binary` but if you place this name it'll get an error while if you expand the task (an arrow beside its name) it'll show `Minecraft 1.13.2` and that'll work.  
Use command `python Main.py -h` or `python Main.py --help` to show some help with command line arguments.  
For minecraft users: press F3 + p to disable the pause menu when you change the focus (use windows key or alt + tab to change window).

## Requirements

Python 3 (tested with 3.7).  
For libraries check the file `requirements.txt` or run the command `pip install -r requirements.txt`.