#!python

# System Imports
import os
import time

# Third Party Imports
import pyautogui
import PIL
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
        in_carousel = pyautogui.locateOnScreen('resources/carousel.PNG', confidence=0.9,
                                               region=(0, TOP_BAR_THICKNESS, RES[0], RES[1])) is not None
        gray_helmet = pyautogui.locateOnScreen('resources/helmet.PNG', confidence=helmet_confidence,
                                               region=(0, TOP_BAR_THICKNESS, RES[0], RES[1])) is not None
        blue_helmet = pyautogui.locateOnScreen('resources/helmetblue.PNG', confidence=helmet_confidence,
                                               region=(0, TOP_BAR_THICKNESS, RES[0], RES[1])) is not None
        augment_button = pyautogui.locateOnScreen('resources/augmentbutton.PNG', confidence=0.9,
                                                  region=(0, TOP_BAR_THICKNESS, RES[0], RES[1])) is not None
        enemy_bench_empty = pyautogui.locateOnScreen('resources/emptybench.PNG', confidence=0.8,
                                                     region=(0, TOP_BAR_THICKNESS, RES[0], RES[1])) is not None
        planning = blue_helmet or gray_helmet and not in_carousel and not augment_button and enemy_bench_empty
        print(
            f"bluehelm {blue_helmet} grayhelm {gray_helmet} incarousel {in_carousel} augment_button {augment_button}"
            f" enemybenchempty {enemy_bench_empty}")
        if planning:
            print("in planning phase")
            filename = f"{RAW_SCREENSHOT_DIR}\\{next}.png"
            im = pyautogui.screenshot(filename, region=(0, TOP_BAR_THICKNESS, RES[0], RES[1]))
            next += 1
            time.sleep(1)
