"""
TFT Assistant
"""
import time
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import PIL.Image as Image
import PIL.ImageGrab as ImageGrab
import uuid
import asyncio
import pygetwindow as gw
from pathlib import Path
from .predictor.Predictor import Predictor
from .recommender.Recommender import Recommender
import sys
# fix briefcase stupid shit
try:
    import win32gui
    import win32ui
    import win32con
    from ctypes import windll
    
except ModuleNotFoundError:
    print("Try to find 'app_packages' folder and to add this to python's 'site' package.")
    app_packages = ""
    for path in sys.path:
        if path.endswith("app_packages"):
            app_packages = path
    if app_packages == "":
        print("Couldn't find 'app_packages' folder.")
        raise ModuleNotFoundError
    else:
        
        import site
        site.USER_SITE = app_packages  # correct the 'site-packages' path to 'app_packages' path
        site.main()  # recall site package thus all .pth in 'app_packages' will be add to sys.path
        import win32gui
        import win32ui
        import win32con
        from ctypes import windll
    for path in sys.path:
        print(path)
# end fix briefcase stupid shit

class TFTInterpreter(toga.App):
    here = Path(__file__).parent
    print("What the fuck")
    labels_path = here/"predictor/static/set6_classes.csv"
    model_path = here/"predictor/static/set6_best_model.pth"
    perfects_path = here/"recommender/static/set6_perfect_synergies.json"
    # check the paths exist
    if not labels_path.exists():
        print("Couldn't find labels file.")
        print(str(labels_path))
        raise FileNotFoundError
    if not model_path.exists():
        print("Couldn't find model file.")
        print(str(model_path))
        raise FileNotFoundError
    if not perfects_path.exists():
        print("Couldn't find perfects file.")
        print(str(perfects_path))
        raise FileNotFoundError

    predictor = Predictor(str(labels_path), str(model_path))
    recommender = Recommender(str(labels_path), str(perfects_path))
    def get_tft_window_screenshot(self) -> Image.Image:
        # returns a screenshot of the TFT window as a PIL image
        window_name = "League of Legends (TM) Client"
        hwnd = win32gui.FindWindow(None, window_name)

        # get the window offset from the top left corner
        rect = win32gui.GetWindowRect(hwnd)
        window_height = rect[3] - rect[1]
        window_width = rect[2] - rect[0]
        print("Width and height from getwindowrect")
        print(window_width, window_height)
        print('rect: ', rect)

        # get just the window (not including the title bar)
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top
        # magic numbers riina and I figured out
        boff = 45 
        loff = 11 

        left = rect[0]
        top = rect[1]
        top = top + boff
        left = left + loff

        win32gui.SetForegroundWindow(hwnd)
        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        if result == None:
            #PrintWindow Succeeded
            return im

    def get_rec(self):
        """
        Get the recommendations from the TFT window.
        Args:
            self: the current gui object
        Returns:
            string of recommendations based on the units on the board
        """
        im = self.get_tft_window_screenshot()
        p = self.predictor.predict_on_image(im)
        return p 
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        windll.shcore.SetProcessDpiAwareness(1)
        row_1 = toga.Box(style=Pack(direction=COLUMN))
        # label for units
        units_label = toga.Label('Units: ', style=Pack(padding=5))
        unit_text = toga.MultilineTextInput(readonly=True, style=Pack(height=120))
        row_1.add(units_label)
        row_1.add(unit_text)
        row_2 = toga.Box(style=Pack(direction=COLUMN))
        # label for recommendations
        rec_label = toga.Label('Recommendations: ', style=Pack(padding=5))
        rec_text = toga.MultilineTextInput(readonly=True, style=Pack(height=240))
        row_2.add(rec_label)
        row_2.add(rec_text)
        row_3 = toga.Box(style=Pack(direction=COLUMN)) 
        # button to get recommendations
        async def get_recommendations(widget):
            # async get units
            units = await asyncio.to_thread(self.get_rec)
            # async recommend units
            recs = await asyncio.to_thread(self.recommender.get_closest_matches, units[0])
            # format the units and recommendations
            un_abb_units = list(map(lambda x: self.recommender.abb_to_full[x], units[0]))
            units_txt ="\n".join(un_abb_units)
            print("NEW UNITS TEXT")
            print(units_txt)
            recs_txt = ""
            for r in recs:
                recs_txt += f"Team size: {r}\n"
                for team in recs[r]:
                    using = set(un_abb_units).intersection(set(team))
                    print("TEAM")
                    print(set(un_abb_units))
                    print("PERF")
                    print(team)
                    needs = set(team).difference(using)
                    recs_txt += f"TEAM:\n"
                    recs_txt += "HAVE: " + ", ".join(using) + "\n"
                    recs_txt += "NEED: " + ", ".join(needs) + "\n"
            # update the text on the ui
            unit_text.value = units_txt
            rec_text.value = recs_txt
        button = toga.Button(
            'Get Recommendations',
            on_press=get_recommendations,
            style=Pack(padding=5)
        )
        row_3.add(button)

        main_box = toga.Box(style=Pack(direction=COLUMN), children=[row_1, row_2, row_3])
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return TFTInterpreter()