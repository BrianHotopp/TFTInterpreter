from turtle import left
import pyautogui
import numpy
import uuid
import cv2
import time

def get_top_numbers():
    top_offset = 58
    left_offset = 755
    width_of_numbers = 55 
    height_of_numbers = 38
    im2 = pyautogui.screenshot(
        region=(
            left_offset,
            top_offset,
            width_of_numbers,
            height_of_numbers
        ))
    return im2

if __name__ == "__main__":
    # full screen
    #im = pyautogui.screenshot("test.png", region=(0,offset, 1920, 1080))
    while True:
        # check if the top numbers changed
        lastPIL = get_top_numbers()
        time.sleep(1)
        newPIL = get_top_numbers()
        open_cv_image1 = numpy.array(lastPIL)
        open_cv_image1 = open_cv_image1[:, :, ::-1].copy()  
        open_cv_image2 = numpy.array(newPIL) 
        open_cv_image2 = open_cv_image2[:, :, ::-1].copy() 

        # do with image1
        hist1 = cv2.calcHist([open_cv_image1], [0], None, [256], [0, 256])
        hist1 = cv2.normalize(hist1, hist1).flatten()
        # do with image2
        hist2 = cv2.calcHist([open_cv_image2], [0], None, [256], [0, 256])
        hist2 = cv2.normalize(hist2, hist2).flatten()
        # if compare is > 0 then top numbers changed
        compare = cv2.compareHist(hist1, hist2, 1) 
        offset = 58
        # check to make sure we are not in a carousel round
        im = pyautogui.locateOnScreen('resources/noncarousel.PNG')
        planning_phase = compare > 0 and im is not None
        if planning_phase:
            print("in planning phase")
            for i in range(5):
                print("take screenshot")
                time.sleep(1)
        else:
            print("not in planning phase")
        