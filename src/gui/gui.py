#!python
# Third Party Imports
import datetime
import tkinter as tk
import mouse
import keyboard
import threading
import time
import uuid
# Local Imports
from buttons_clicked import Clicks


class TFT_GUI:
    """
    so I think there are 2 functions you can assume we will have implemented for you
    query_game_state() -> dict[str, any] with four key, value pairs
    "units_on_board" that contains list[str] of the units on the board
    "level" that contains an int for the player's level
    "gold" that contains an int for the player's gold
    "hp" that contains an int for the player's current hp
    get_recommendation(units_on_board: list[str]) -> dict[str, float]
    giving you a dict of recommended units to buy and some kind of rating for each recommended unit
    """

    def __init__(self) -> None:
        """
        Initialize the GUI.
        Args:
            self: the current gui object
        """
        # get window handle and set League Client as foreground
        self.window_name = "League of Legends (TM) Client"
        """
        hwnd = win32gui.FindWindow(None, self.window_name)
        win32gui.ShowWindow(hwnd, 1)
        win32gui.SetForegroundWindow(hwnd)

        # get points and dimensions of window
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        """

        self.master = tk.Tk()
        # change title
        self.master.title("The Interpreter")
        # set icon for master window
        try:
            self.master.iconbitmap("../favicon.ico")
        except:
            print("Couldn't load icon.")

        self.master.geometry(f"{500}x{200}")

        # create variables to check for widgets clicked
        self.c = Clicks()

        # add buttons
        # label2 = tk.Label(self.master, text="Label2").pack(side="left")
        # tk.Button(self.master, text="Quit", command=self.do_nothing).pack(side="right")
        # tk.Button(self.master, text="Hide", command=self.do_nothing).pack(side="right")

        # add mouse clicks
        # create menu bar
        menubar = tk.Menu(self.master)

        # create file menu items
        filemenu = tk.Menu(menubar, tearoff=0, postcommand=self.file_menu)
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Auto Save")
        filemenu.add_separator()

        # create sub menu for preferences
        submenu = tk.Menu(filemenu, tearoff=0)
        submenu.add_command(label="Settings")
        submenu.add_command(label="Keyboard Shortcuts")
        filemenu.add_cascade(label="Preferences", menu=submenu)
        filemenu.add_separator()

        filemenu.add_command(label="Hide Widgets Only")
        filemenu.add_command(label="Hide Window")
        filemenu.add_command(label="Exit", command=self.quit_program)
        menubar.add_cascade(label="File", menu=filemenu)

        # create show menu items
        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Statistics")
        runmenu.add_command(label="Suggestions")
        menubar.add_cascade(label="Show", menu=runmenu)

        # create help menu items
        helpmenu = tk.Menu(menubar, tearoff=0, postcommand=self.help)
        helpmenu.add_command(label="Help Index", command=self.help_index)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        # configure the window
        self.master.config(menu=menubar)
        """
        do live inference on a second thread, code mostly from 
        https://stackoverflow.com/questions/64287940/update-tkinter-gui-from-a-separate-thread-running-a-command
        """
        self.units_on_board = tk.StringVar(self.master, "Units currently on the board")
        self.lbl = tk.Label(self.master, text="Start")
        self.lbl.pack(side="top")
        thd = threading.Thread(target=self.timecnt)
        thd.daemon = True
        thd.start()
        self.master.bind("<<event1>>", self.eventhandler)
        self.master.mainloop()
        # when the ui dies, wait for the async thread to finish
        thd.join()

    def timecnt(self):  # runs in background thread
        print('Timer Thread', threading.get_ident())  # background thread id
        for x in range(10):
            self.master.event_generate("<<event1>>", when="tail", state=123)  # trigger event in main thread
            self.units_on_board.set(' ' * 15 + str(x))  # update text entry from background thread
            time.sleep(1)  # one second

    def eventhandler(self, evt):  # runs in main thread
        print('Event Thread', threading.get_ident())  # event thread id (same as main)
        print(evt.state)  # 123, data from event
        string = datetime.datetime.now().strftime('%I:%M:%S %p')
        self.lbl.config(text=string)  # update widget
        # txtvar.set(' '*15 + str(evt.state))  # update text entry in main thread

    def file_menu(self) -> None:
        """
        Account for the file menu being clicked.
        Args:
            self: the current gui object
        """
        self.c.file = True
        self.master.after(100, self.file_menu)

    def help(self) -> None:
        """
        Account for the help menu being clicked.
        Args:
            self: the current gui object
        """
        self.c.help = True
        self.master.after(100, self.help)

    def help_index(self) -> None:
        """
        Account for the help index button being clicked.
        Args:
            self: the current gui object
        """
        self.c.help_index = True
        self.master.after(100, self.help_index)

    def about(self) -> None:
        """
        Account for the about button being clicked.
        Args:
            self: the current gui object
        """
        self.c.about = True
        top = tk.Toplevel(self.master)
        top.geometry(f"{400}x{200}")
        top.title("About")
        # add about text
        about_text = """We are a group of students at RPI who originally 
            designed this for a class.\n The goal of the TFT Interpreter was
            to create a product similar to other overlays that currently 
            exist without the extensive and heavy installations"""
        tk.Label(top, text="About Us").pack()
        tk.Label(top, text=about_text).pack()

    def hide_about(self, top: tk.Toplevel) -> None:
        """
        Account for the close button being clicked in the about menu.
        Args:
            self: the current gui object
            top: the top window created (for about)
        """
        self.c.close_about = True
        top.destroy()

    def quit_program(self) -> None:
        """
        Quit the whole program.
        Args:
            self: the current gui object
        """
        self.c.quit = True
        self.master.quit()
