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

def find_typos(location, units):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    # the elements of this list represent rows of a csv
    temp_res = []
    counts = dict()
    # Run through all the files
    non = set()
    for file in os.listdir(location):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Open the xml name
        tree = ET.parse(file_whole_name)
        root = tree.getroot()
        # Find all the bounding objects
        print("Printing potential typos...")
        for label_object in root.findall("object"):
            # Class label
            classname = label_object.find("name").text
            if classname not in units.values():
                print(classname)

def crawl_labels(location, dry_run):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    # the elements of this list represent rows of a csv
    temp_res = []
    counts = dict()
    # Run through all the files
    non = set()
    for file in os.listdir(location):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Open the xml name
        tree = ET.parse(file_whole_name)
        root = tree.getroot()
        # Find all the bounding objects
        for label_object in root.findall("object"):
            # Class label
            classname = label_object.find("name").text
            if classname not in SET_6_UNITS.values():
                if classname in typos.keys():
                    label_object.find("name").text = typos[classname]
                else:
                    non.add(classname)
                    if dry_run:
                        print(f"would have removed the label object with name {classname}, but this is a dry run. Change code under me to perform destructive operations.") 
                    else:
                        print(f"Removing label object with name {classname}.")
                        root.remove(label_object)
        if len(root.findall("object")) == 0:
            # we might have removed some object and left the current xml file with no objects
            # in that case remove the xml file
            if not dry_run:
                os.remove(file_whole_name)
        if not dry_run:
            print(f"Writing xml file.")
            tree.write(file_whole_name)

if __name__ == "__main__":
    """
    this program goes through a directory of xml files and attempts to fix typo'd label names
    it takes a labels directory, a set file, and a typos file
    it goes through each xml file in the labels directory and checks each label;
    if the label is not found in the list of units passed in the set file, it attempts to replace it with some substitution from the typos file
    it can also be used to find potential typos in the class names of xml files - simply exclude the typos-file argument
    """
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    arg_p.add_argument("-s", "--set_file",
                       required=True,
                       type=str,
                       help="path to csv file containing unit names and abbreviations for the desired set")

    arg_p.add_argument("-t", "--typos_file",
                       required=False,
                       type=str,
                       help="path to csv file containing typo'd spelling and correct spelling for units")

    arg_p.add_argument("-d", "--dry_run",
                       required=False,
                       type=bool,
                       default=True, 
                       help="flag; tells us whether or not to do a dry-run")
    
    args = vars(arg_p.parse_args())

    # read set 6 units in 
    SET_6_UNITS = dict()
    with open(args["set_file"]) as classes_file_handle:
        for line in classes_file_handle.readlines():
            unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
            SET_6_UNITS[unit_name] = abbreviated_name
    if "typos_file" in args:
        # load the optional typos file
        TYPOS = dict()
        with open(args["typos_file"]) as typos_file_handle:
            for line in typos_file_handle.readlines():
                typod_name, correct_name = [x.strip() for x in line.split(",")]
                TYPOS[typod_name] = correct_name 

        crawl_labels(args["local_labels_dir"], args["dry_run"])
    else:
        find_typos(args["local_labels_dir"], SET_6_UNITS)
