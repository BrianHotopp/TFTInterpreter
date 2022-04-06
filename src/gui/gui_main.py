#!/usr/bin/env python3.9
# Third Party Imports
import psutil

# Local Imports
from src.gui.gui import TFT_GUI

# download requirements for a specific folder
# pipreqs path/to/project
# autopytoexe (for creating exe)

# needed to install from the download (python 3.9, x64)
# https://github.com/mhammond/pywin32/releases

# pyinstaller --onefile C:\Users\gwyne\Documents\GitHub\TFTInterpreter\gui\gui_main.py -w

# TO DO:
# - add in widget/box for statistics
# - add in widget/box for analytics (suggestions)
# - create exe

if __name__ == "__main__":
    # only run the GUI if the League Client is open
    #if "LeagueClient.exe" in (i.name() for i in psutil.process_iter()):
    if True:
        g = TFT_GUI()
    else:
        print("League client not open")