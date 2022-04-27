#!python

# System Imports
import os

# Third Party Imports
import pyautogui
import PIL

# Global Variables
TOP_BAR_THICKNESS = 58
RES = [1920, 1080]
RAW_SCREENSHOT_DIR = "../../datadump/TFTInterpreterData/raw/"

def get_top_numbers() -> PIL.PIL.Image:
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
    helmet_confidence = 0.6 
    # get the next image id
    next = 1+max([int(x.split(".")[0]) for x in list(os.listdir(RAW_SCREENSHOT_DIR))])
    while True:
            input()
            print("taking screenshot to")
            filename = f"{RAW_SCREENSHOT_DIR}{next}.png"
            im = pyautogui.screenshot(filename, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1]))
            next +=1

            print(f"saved file {filename}")
