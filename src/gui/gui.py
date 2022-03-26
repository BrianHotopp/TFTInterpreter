#!python

# Third Party Imports
import tkinter as tk
import keyboard
import threading
import PIL
from win32 import win32gui

# Local Imports
from src.app.continuous_inference import Predictor

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
        self.master = tk.Tk()
        self.master.title("The Interpreter")

        # set icon
        try:
            self.master.iconbitmap("favicon.ico")
        except:
            print("Couldn't load icon.")

        self.window_name = "League of Legends (TM) Client"

        left, top, right, bottom = self.get_tft_window_loc()
        width = right - left
        height = bottom - top
        self.master.geometry(f"{width}x{height}")
        self.getting_units = False

        # this variable is mutated in the threads
        self.board_state = dict()

        # thread to get the board state
        self.thd = None

        # todo handle these paths less like an idiot
        labels_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\code\src\gather_data\\resources\set6_classes.txt"
        model_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\code\src\models\\10epoch.pth"
        self.predictor = Predictor(labels_path, model_path)

        # keybinds
        keyboard.add_hotkey("ctrl+q", lambda: self.quit_program)
        keyboard.add_hotkey("alt+`", lambda: self.show_hide)

        # create menu bar
        menubar = tk.Menu(self.master)

        self.image_index = 1

        # create file menu items
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save_image)
        filemenu.add_separator()

        # create sub menu for preferences
        submenu = tk.Menu(filemenu, tearoff=0)
        submenu.add_command(label="Settings")
        submenu.add_command(label="Keyboard Shortcuts", command=self.shortcuts)
        filemenu.add_cascade(label="Preferences", menu=submenu)
        filemenu.add_separator()

        filemenu.add_command(label="Hide Window", command=self.hide_window)
        filemenu.add_command(label="Exit", command=self.quit_program)
        menubar.add_cascade(label="File", menu=filemenu)

        # create show menu items
        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Statistics")
        runmenu.add_command(label="Suggestions", command=self.show_analytics)
        menubar.add_cascade(label="Show", menu=runmenu)

        # create help menu items
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.help_index)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # configure the window
        self.master.config(menu=menubar)
        self.units_on_board = tk.StringVar(self.master, "Units currently on the board")
        self.lbl = tk.Label(self.master, textvar=self.units_on_board)
        self.lbl.pack(side="top")
        self.master.after(100, self.update_board_state)
        self.master.mainloop()

        # RuntimeError after closing might be fixable
        # it's happening because the thread for running continuous inference tries to mutate data from the GUI thread
        # after the GUI thread dies
        # https://stackoverflow.com/questions/62919494/main-thread-is-not-in-main-loop

    def get_tft_window_loc(self) -> tuple:
        """
        Get the location of the TFT window.
        Args:
            self: the current gui object
        Returns:
            window rectangle in terms of left, top, right, bottom
        """
        hwnd = win32gui.FindWindow(None, self.window_name)
        # get points and dimensions of window
        bbox = win32gui.GetWindowRect(hwnd)
        return bbox

    def get_tft_window_screenshot(self) -> PIL.Image.Image:
        """
        Get the screenshot of the TFT window.
        Args:
            self: the current gui object
        Returns:
            image object
        """
        im = PIL.ImageGrab.grab(self.get_tft_window_loc())
        return im

    def save_image(self) -> None:
        """
        Save the screenshot.
        Args:
            self: the current gui object
        """
        im = self.get_tft_window_screenshot()
        filename = f"tft_screenshot{self.image_index}"
        im = im.save(filename)
        image_index += 1

    def get_units_thread(self) -> None:
        """
        Gets the units on the board.
        Args:
            self: the current gui object
        """
        # this can take a while to return
        labels, scores = self.predictor.predict_on_image(self.get_tft_window_screenshot())
        # spooky mutation of the parent thread's data
        # only possible because when we call this function from another thread we get
        # a reference to self, ie the parent thread's mutable data
        r = "\n".join([f"{x[0]}:{x[1]}" for x in zip(labels, scores)])
        self.units_on_board.set(r)

    def update_board_state(self) -> None:
        """
        Updates the board state continuously.
        Args:
            self: the current gui object
        """
        # the first time we update the board state the app has no secondary thread
        print("updating boardstate")
        if self.thd is None:
            self.thd = threading.Thread(target=self.get_units_thread, daemon=True)
            self.thd.start()
        elif self.thd.is_alive():
            print("thread doing its thing")
        else:
            self.thd = threading.Thread(target=self.get_units_thread, daemon=True)
            self.thd.start()
        self.master.after(100, self.update_board_state)

    def help_index(self) -> None:
        """
        Show help index.
        Args:
            self: the current gui object
        """
        return None

    def about(self) -> None:
        """
        Account for the about button being clicked.
        Args:
            self: the current gui object
        """
        top = tk.Toplevel(self.master)
        
        # get window size and position
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        x = self.master.winfo_x()
        y = self.master.winfo_y()

        # size to half the current window, position in the middle of the screen
        new_width = window_width // 2
        new_height = window_height // 2
        top.geometry(f"{new_width}x{new_height}+{x + new_width//2}+{y + new_height//2}")

        top.title("About")
        # add about text
        about_text = """We are a group of students at RPI who originally 
            designed this for a class.\n The goal of the TFT Interpreter was
            to create a product similar to other overlays that currently 
            exist without the extensive and heavy installations."""
        tk.Label(top, text="About Us").pack()
        tk.Label(top, text=about_text).pack()
        tk.Button(top, text="Close", command=lambda: self.hide_about(top)).pack()

    def hide_about(self, top: tk.Toplevel) -> None:
        """
        Account for the close button being clicked in the about menu.
        Args:
            self: the current gui object
            top: the top window created (for about)
        """
        top.destroy()

    def show_hide(self) -> None:
        """
        The command for showing and hiding the whole GUI.
        Args:
            self: the current gui object
        """
        if self.master.winfo_viewable():
            self.master.withdraw()
        else:
            self.master.wm_deiconify()
            self.master.lift()
            self.master.attributes("-topmost", True)

    def shortcuts(self) -> None:
        """
        Shows all the keyboard shortcuts.
        Args:
            self: the current gui object
        """
        tk.Label(self.master, text="Keyboard Shortcuts").pack()

    def show_analytics(self) -> None:
        """
        Show the units suggested to buy.
        Args:
            self: the current gui object
        """
        # these are the units currently on the board:
            # unit1,
            # unit2,
            # unit3
        # these are the units you should buy:
            # unit1,
            # unit2,
            # unit3
        tk.Label(self.master, text="These are the units currently on the board:").pack()
        tk.Label(self.master, text="These are the units you should buy:").pack()

    def hide_window(self) -> None:
        """
        The command for hiding the window.
        Args:
            self: the current gui object
        """
        if self.master.winfo_viewable():
            self.master.withdraw()

    def quit_program(self) -> None:
        """
        Quit the whole program.
        Args:
            self: the current gui object
        """
        self.master.quit()
