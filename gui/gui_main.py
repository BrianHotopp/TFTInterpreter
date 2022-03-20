#!python
# Third Party Imports
import psutil

# Local Imports
from gui import TFT_GUI


if __name__ == "__main__":
    # only run the GUI if the League Client is open
    if "LeagueClient.exe" in (i.name() for i in psutil.process_iter()):
        g = TFT_GUI()