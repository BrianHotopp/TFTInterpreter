#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: rmallunlabeled.py
Author: Brian Hotopp 
Contact: brihoto@gmail.com  
Time: 2022.02.25
"""
import shutil
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
# typos that I made during data entry
typos = dict()
typos["quinn"] = "quin"
typos["leona"] = "leon"
typos["silco"] = "silc"
typos["syra"] = "zyra"
typos["brand"] = "bran"
typos["lcui"] = "luci"
typos["poppy"] = "popp"


def crawl_labels(annotation_dir):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    # the elements of this list represent rows of a csv
    temp_res = []
    counts = dict()
    # Run through all the files
    non = set()
    i = 0
    for file in os.listdir(annotation_dir):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        annotation_full_path = f"{annotation_dir}\{file}"

        # Open the xml name
        tree = ET.parse(annotation_full_path)
        root = tree.getroot()

        old_image_filename = tree.find("filename").text
        new_image_filename = f"{i}.png"
        old_image_full_path = f"E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\{old_image_filename}"
        new_image_full_path = f"E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\{new_image_filename}"
        annotation_new_full_path = f"{annotation_dir}\{i}.xml" 

        # change the image filename in the annot
        print(f"changing image filename from \n{old_image_filename} to \n{new_image_filename}")
        tree.find("filename").text = new_image_filename
        # change the image path in the annot
        print(f"changing image path in annotation from \n{old_image_full_path} to \n{new_image_full_path}")
        tree.find("path").text = f"E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\{new_image_filename}"
        # save the annot
        tree.write(annotation_full_path)
        # change the annot filename 
        print(f"renaming the annotation file on disk from \n{annotation_full_path} to \n{annotation_new_full_path}")
        os.rename(annotation_full_path, annotation_new_full_path)
        # change the image filename
        print(f"changing the image file on disk from \n{old_image_full_path} to \n{new_image_full_path}")
        os.rename(old_image_full_path,new_image_full_path)
        i+=1
# change the image filename in the annot
# change the image path in the annot
# change the annot filename on disk
# change the image filename ondisk

if __name__ == "__main__":
    # Add the argument parse
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    args = vars(arg_p.parse_args())
    crawl_labels(args["local_labels_dir"])
