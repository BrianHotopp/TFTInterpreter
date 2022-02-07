import pyautogui
import numpy
import uuid
import cv2
import time
offset = 125

im = pyautogui.screenshot("test.png", region=(0,offset, 1920, 1080))