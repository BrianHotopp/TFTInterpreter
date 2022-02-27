import pyautogui
import numpy
import uuid
import cv2
import time
TOP_BAR_THICKNESS = 58
RES = [1920, 1080]
RAW_SCREENSHOT_DIR = "data/raw/"
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
        in_carousel = pyautogui.locateOnScreen('resources/carousel.PNG', confidence = 0.9, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1])) != None
        gray_helmet = pyautogui.locateOnScreen('resources/helmet.PNG', confidence = helmet_confidence, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1])) != None
        blue_helmet = pyautogui.locateOnScreen('resources/helmetblue.PNG', confidence = helmet_confidence, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1])) != None
        augment_button = pyautogui.locateOnScreen('resources/augmentbutton.PNG', confidence = 0.9, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1])) != None
        enemy_bench_empty = pyautogui.locateOnScreen('resources/emptybench.PNG', confidence = 0.8, region=(0,TOP_BAR_THICKNESS, RES[0], RES[1])) != None
        planning = blue_helmet or gray_helmet and not in_carousel and not augment_button and enemy_bench_empty
        print(f"bluehelm {blue_helmet} grayhelm {gray_helmet} incarousel {in_carousel} augment_button {augment_button} enemybenchempty {enemy_bench_empty}")
        if planning:
            print("in planning phase")
            im = pyautogui.screenshot(RAW_SCREENSHOT_DIR+str(uuid.uuid4())+".png", region=(0,TOP_BAR_THICKNESS, RES[0], RES[1]))
            time.sleep(1)

