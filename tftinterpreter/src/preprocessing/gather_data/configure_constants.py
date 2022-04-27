#!python

# Third Party Imports
import pyautogui

if __name__=='__main__':
    offset = 125
    im = pyautogui.screenshot("test.png", region=(0,offset, 1920, 1080))