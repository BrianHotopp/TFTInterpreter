#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: cleaner.py
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
#print(SET_6_UNITS)
typos = dict()
typos["quinn"] = "quin"
typos["leona"] = "leon"
typos["silco"] = "silc"
typos["syra"] = "zyra"
typos["brand"] = "bran"
typos["lcui"] = "luci"


def cleanxml(location):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    # the elements of this list represent rows of a csv
    temp_res = []
    counts = dict()
    # Run through all the files
    non = set()
    i = 0
    for file in os.listdir(location):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Open the xml name
        tree = ET.parse(file_whole_name)
        root = tree.getroot()
        if root.find("folder").text != "raw":
            root.find("folder").text = "raw"
            filename = root.find("filename")
            root.find("path").text = f"E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\{filename.text}"
            i+=1
        tree.write(file_whole_name)
    print(f"changed {i} files")


if __name__ == "__main__":
    # Add the argument parse
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    args = vars(arg_p.parse_args())
    cleanxml(args["local_labels_dir"])
