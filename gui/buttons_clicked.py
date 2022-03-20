#!python
class Clicks:
    """
    The clicks class is utilized by the GUI when trying to determine
    whether or not a button has been clicked. The purpose is mainly
    for when a user clicks out of the GUI window AND the League Client
    is open. It will then tell the GUI to close the window as it is
    not needed to be open.
    """
    def __init__(self):
        """
        Initialize the status of all the buttons to false.
        Args:
            self: the current clicks object created
        """
        self.quit = False
        self.hide = False
        self.help = False
        self.help_index = False
        self.about = False
        self.file = False
        self.close_about = False

    def check_clicks(self):
        """
        Check if any button has been clicked. If yes, return false. If no, return true.
        Args:
            self: the current clicks object
        Returns: boolean for if any button has been clicked
        """
        if self.quit == self.hide == self.help == self.help_index \
            == self.about == self.file == self.close_about == False:
            return True
        return False

    def reset(self):
        """
        Reset all the clicks to be false (no button is being clicked).
        Args:
            self: the current clicks object
        """
        self.quit = False
        self.hide = False
        self.help = False
        self.help_index = False
        self.about = False
        self.file = False
        self.close_about = False
