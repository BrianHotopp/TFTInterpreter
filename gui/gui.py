#!python
# Third Party Imports
import tkinter as tk
from win32 import win32gui
import mouse
import keyboard

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
    def __init__(self):
        """
        Initialize the GUI.
        Args:
            self: the current gui object
        """
        # get window handle and set League Client as foreground
        hwnd = win32gui.FindWindow(None, "League of Legends")
        win32gui.ShowWindow(hwnd, 1)
        win32gui.SetForegroundWindow(hwnd)

        # get points and dimensions of window
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        self.master = tk.Tk()

        # remove top bar
        self.master.overrideredirect(True)

        # change title
        self.master.title("The Interpreter")

        # adjust window geometry to account for top bar
        new_y = top-20
        self.master.geometry(f"{width}x{height}+{left}+{new_y}")

        # transparent backgroun to make it an overlay
        self.master.config(bg = '#add123')
        self.master.wm_attributes('-transparentcolor','#add123')

        # create variables to check for widgets clicked
        self.c = Clicks()

        # add buttons
        # label1 = tk.Label(self.master, text="Label1").pack(side="bottom")
        # label2 = tk.Label(self.master, text="Label2").pack(side="left")
        # tk.Button(self.master, text="Quit", command=self.do_nothing).pack(side="right")
        # tk.Button(self.master, text="Hide", command=self.do_nothing).pack(side="right")

        # add keyboard hotkeys (keybinds)
        keyboard.add_hotkey('alt+`', lambda: self.show_hide())
        keyboard.add_hotkey('ctrl+q', lambda: self.master.quit())
        keyboard.add_hotkey('alt+tab', lambda: self.alt_tab())

        # add mouse clicks
        mouse.on_click(lambda: self.mouse_click())
        mouse.on_right_click(lambda: self.mouse_click())
        mouse.on_middle_click(lambda: self.mouse_click())

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

        # show tkinter window on top of tft client
        self.master.lift()
        self.master.wm_attributes("-topmost", 1)
        self.master.mainloop()

    def show_hide(self):
        """
        The command for showing and hiding the whole GUI.
        Args:
            self: the current gui object
        """

        # make sure the League Client is in the foreground
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) \
            == "League of Legends":
            # if the window can be seen, hide it.
            # if not, show it.
            if self.master.winfo_viewable():
                self.master.withdraw()
            else:
                self.master.wm_deiconify()
                self.master.lift()
                self.master.attributes("-topmost", True)

    def alt_tab(self):
        """
        This function is called whenever the user clicks alt+tab on the keyboard.
        Args:
            self: the current gui object
        """
        # if the GUI is viewable and the Client is in the foreground, hide.
        if self.master.winfo_viewable():
            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) \
                != "League of Legends":
                self.master.withdraw()
        else:
            self.show_hide()

    def mouse_click(self):
        """
        This function is called to withdraw if a click is registered outside the GUI.
        Args:
            self: the current gui object
        """
        # CLICK DOESN'T WORK AFTER "ABOUT" IS PRESSED AND CLOSED

        # if the buttons haven't been clicked (means a click is outside the GUI)
        if self.c.check_clicks():
            # if the window is currently visible, hide if League Client is not in the foreground.
            if self.master.winfo_viewable():
                if win32gui.GetWindowText(win32gui.GetForegroundWindow()) \
                    != "League of Legends":
                    self.master.withdraw()

        # reset global variables to false
        self.c.reset()

    def file_menu(self):
        """
        Account for the file menu being clicked.
        Args:
            self: the current gui object
        """
        self.c.file = True
        self.master.after(100, self.file_menu)

    def help(self):
        """
        Account for the help menu being clicked.
        Args:
            self: the current gui object
        """
        self.c.help = True
        self.master.after(100, self.help)

    def help_index(self):
        """
        Account for the help index button being clicked.
        Args:
            self: the current gui object
        """
        self.c.help_index = True
        self.master.after(100, self.help_index)

    def about(self):
        """
        Account for the about button being clicked.
        Args:
            self: the current gui object
        """
        self.c.about = True
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
        tk.Label(top, text="About Us").pack()
        tk.Label(top, text="We are a group of students at RPI who originally \
            designed this for a class.\nThe goal of the TFT Interpreter was \
            to create a product similar to other overlays\nthat currently \
            exist without the extensive and heavy installations.").pack()
        tk.Button(top, text="Close", command=lambda: self.hide_about(top)).pack()

    def hide_about(self, top: tk.Toplevel):
        """
        Account for the close button being clicked in the about menu.
        Args:
            self: the current gui object
            top: the top window created (for about)
        """
        self.c.close_about = True
        top.destroy()

    def quit_program(self):
        """
        Quit the whole program.
        Args:
            self: the current gui object
        """
        self.c.quit = True
        self.master.quit()
