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
import pyautogui
from src.app.continuous_inference import Predictor
from PIL import ImageGrab
from buttons_clicked import Clicks
import win32gui


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

        self.master = tk.Tk()
        # change title
        self.master.title("The Interpreter")
        # set icon for master window
        try:
            self.master.iconbitmap("../favicon.ico")
        except:
            print("Couldn't load icon.")
        self.window_name = "League of Legends (TM) Client"
        self.master.geometry(f"{500}x{200}")
        self.getting_units = False
        # this variable is mutated in the threads
        self.board_state = dict()
        # thread to get the board state
        self.thd = None
        # create variables to check for widgets clicked
        self.c = Clicks()
        # todo handle these paths less like an idiot
        labels_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\code\src\gather_data\\resources\set6_classes.txt"
        model_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\code\src\models\\10epoch.pth"
        self.predictor = Predictor(labels_path, model_path)
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
        self.units_on_board = tk.StringVar(self.master, "No units currently detected on the board")
        self.lbl = tk.Label(self.master, textvar=self.units_on_board)
        self.lbl.pack(side="top")
        self.master.after(100, self.update_board_state)
        self.master.mainloop()
        # RuntimeError after closing might be fixable
        # it's happening because the thread for running continuous inference tries to mutate data from the GUI thread
        # after the GUI thread dies
        # https://stackoverflow.com/questions/62919494/main-thread-is-not-in-main-loop

    def get_tft_window_loc(self):
        """
        gets the location of the tft window using win32
        """
        hwnd = win32gui.FindWindow(None, self.window_name)
        # get points and dimensions of window
        bbox = win32gui.GetWindowRect(hwnd)
        return bbox

    def get_tft_window_screenshot(self):
        im = ImageGrab.grab(self.get_tft_window_loc())
        return im

    def get_units_thread(self):
        # this can take a while to return
        ss = self.get_tft_window_screenshot()
        in_planning_phase = self.predictor.in_planning_phase(ss)
        if in_planning_phase:
            labels, scores = self.predictor.predict_on_image(ss)
            # spooky mutation of the parent thread's data
            # only possible because when we call this function from another thread we get
            # a reference to self, ie the parent thread's mutable data
            results = [f"{x[0]}:{x[1]:.2f}" for x in zip(labels, scores)]
            r = "\n".join(results[:min(len(results), 10)])
            self.units_on_board.set(r)
            return
        else:
            r = "Not currently in the planning phase"
            self.units_on_board.set(r)
            return

    def update_board_state(self):
        """
        this function gets called repeatedly in the tkinter event loop
        """
        # the first time we update the board state the app has no secondary thread
        if self.thd is None:
            self.thd = threading.Thread(target=self.get_units_thread, daemon=True)
            self.thd.start()
        elif not self.thd.is_alive():
            self.thd = threading.Thread(target=self.get_units_thread, daemon=True)
            self.thd.start()
        self.master.after(100, self.update_board_state)

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
