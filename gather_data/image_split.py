import numpy as np
import pandas as pd
from pandas import read_csv
import cv2

def read_hex(hex_csv):
    '''
    This function reads the coordinates of a hexagonal shape from a csv.
    '''

    df = read_csv(hex_csv)
    data = df.values
    hex_pts = []
    for i in range(28):
        # vertices of each hexagon
        x1_y1 = [data[i][0], data[i][1]]
        x2_y2 = [data[i][2], data[i][3]]
        x3_y3 = [data[i][4], data[i][5]]
        x4_y4 = [data[i][6], data[i][7]]
        x5_y5 = [data[i][8], data[i][9]]
        x6_y6 = [data[i][10], data[i][11]]
        hex_pts.append([x1_y1, x2_y2, x3_y3, x4_y4, x5_y5, x6_y6])
    return np.array(hex_pts)

def read_rect(rect_csv):
    '''
    This function reads the coordinates of a rectangular shape from a csv.
    '''

    df = read_csv(rect_csv)
    data = df.values
    rect_pts = []
    for i in range(9):
        # vertices of each rectangle
        x1_y1 = [data[i][0], data[i][1]]
        x2_y2 = [data[i][2], data[i][3]]
        x3_y3 = [data[i][4], data[i][5]]
        x4_y4 = [data[i][6], data[i][7]]
        rect_pts.append([x1_y1, x2_y2, x3_y3, x4_y4])
    return np.array(rect_pts)

def crop(img, pts, rect=False):
    '''
    This function crops out the image with the given points and returns the cropped image.
    '''

    # crop bounding rectangle
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    cropped = img[y:y+h, x:x+w].copy()
    if rect:
        return cropped

    # make mask
    pts = pts - pts.min(axis=0)
    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # bitwise and operation
    res = cv2.bitwise_and(cropped, cropped, mask=mask)
    return res

def split_img(file_name):
    '''
    This function splits a TFT screenshot into the different blocks of the planning phase given an image file name.
    It saves the split images to the test_split directory.
    '''

    # open image
    img = cv2.imread(file_name)

    # hexagon coordinates
    hex_pts = read_hex('hex_coords.csv')

    # rectangle coordinates
    rect_pts = read_rect('rect_coords.csv')
    
    # write to png
    for i in range(len(hex_pts)):
        res = crop(img, hex_pts[i])
        path = "test_split/test_hex" + str(i+1) + ".png"
        cv2.imwrite(path, res)

    for j in range(len(rect_pts)):
        res = crop(img, rect_pts[j], rect=True)
        path = "test_split/test_rect" + str(j+1) + ".png"
        cv2.imwrite(path, res)

if __name__ == "__main__":
    split_img("merge_hexes.png")
