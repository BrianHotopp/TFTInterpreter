import pyautogui
import numpy
import uuid
import cv2
import time
import os
TOP_BAR_THICKNESS = 58
RES = [1920, 1080]
RAW_SCREENSHOT_DIR = "../../datadump/TFTInterpreterData/raw/supplemental/"
def get_top_numbers():
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
    #im = pyautogui.screenshot("test.png", region=(0,offset, 1920, 1080))
    helmet_confidence = 0.6 
    while True:
            input()
            print("taking screenshot to")
            filename = RAW_SCREENSHOT_DIR+str(uuid.uuid4())+".png"
            im = pyautogui.screenshot(filename, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1]))
            print(f"saved file {filename}")

