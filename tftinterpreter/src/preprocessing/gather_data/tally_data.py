#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: tally_data.py
Author: Brian Hotopp 
Contact: brihoto@gmail.com  
Time: 2022.02.25
"""

import os
import argparse
import codecs

import pandas as pd
# read set 6 units in 
SET_6_UNITS = dict()
with open("./resources/set6_classes.txt") as classes_file_handle:
    for line in classes_file_handle.readlines():
        unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
        SET_6_UNITS[unit_name] = abbreviated_name



def count_units(location):
    """
    location: the directory where label files are stored
    returns: None, prints the number of training examples we have for each unit
    """
    import xml.etree.ElementTree as ET

    temp_res = []
    # initalize the counts dict
    counts = dict()
    for key in SET_6_UNITS.values():
        counts[key] = 0

    # Run through all the label files
    non = set()
    for file in os.listdir(location):
        # skip files that don't end in .xml
        if not file.endswith(".xml"):
            continue
        # Get the file name
        file_whole_name = f"{location}/{file}"
        # Open the file
        tree = ET.parse(file_whole_name)
        root = tree.getroot()

        # Get the width, height of images
        #  to normalize the bounding boxes
        size = root.find("size")
        width, height = float(size.find("width").text), float(size.find("height").text)

        # Find all the bounding objects
        for label_object in root.findall("object"):
            # Class label
            classname = label_object.find("name").text
            try:
                counts[classname] +=1 
            except:
                print(classname)
                print(file_whole_name)
    # sort the dict and print
    a = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}
    for key in a.keys():
        if a[key] < 1000:
            print(f"{key}:{a[key]}")

if __name__ == "__main__":
    # Add the argument parse
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    args = vars(arg_p.parse_args())
    count_units(args["local_labels_dir"])
