#!python

# System Imports
import os
import time
from pathlib import Path
# Third Party Imports
import pyautogui
import PIL
from src.app.continuous_inference import Predictor
# import numpy
# import uuid
# import cv2

# Global Variables
TOP_BAR_THICKNESS = 58
RES = [1920, 1080]
RAW_SCREENSHOT_DIR = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw"

def get_top_numbers() -> PIL.Image.Image:
    """
    Gets the screenshot
    Returns:
        image object
    """
    left_offset = 755
    width_of_numbers = 55
    height_of_numbers = 38
    im2 = pyautogui.screenshot(
        region=(
            left_offset,
            TOP_BAR_THICKNESS,
            width_of_numbers,
            height_of_numbers
        ))
    return im2

if __name__ == "__main__":
    # full screen
    # im = pyautogui.screenshot("test.png", region=(0,offset, 1920, 1080))
    helmet_confidence = 0.6
    next = 1 + max([int(x.split(".")[0]) for x in list(os.listdir(RAW_SCREENSHOT_DIR))])
    while True:
        im = pyautogui.screenshot(filename, region=(0, TOP_BAR_THICKNESS, RES[0], RES[1]))
        planning = Predictor.in_planning_phase(im)
        if planning:
            print("In planning phase, taking screenshot.")
            filename = Path(f"{RAW_SCREENSHOT_DIR}\\{next}.png")
            im.save(filename)
            print(f"Saved screenshot to {filename}")
            next += 1
        time.sleep(1)
