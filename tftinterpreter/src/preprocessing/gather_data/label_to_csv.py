#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: single_to_multi_dir.py
Author: Brian Hotopp 
Contact: brihoto@gmail.com  
Time: 2022.02.25
"""

import os
import argparse
import codecs

import pandas as pd

def xml2csv(location, path_prefix):
    # To parse the xml files
    import xml.etree.ElementTree as ET

    # Return list
    # the elements of this list represent rows of a csv
    temp_res = []

    # Run through all the files
    for file in os.listdir(location):
        # Check the file name ends with xml
        if not file.endswith(".xml"):
            continue

        # Get the file name
        file_whole_name = f"{location}/{file}"

        # Open the xml name
        tree = ET.parse(file_whole_name)
        root = tree.getroot()

        # Get the width, height of images
        #  to normalize the bounding boxes
        size = root.find("size")
        width, height = float(size.find("width").text), float(size.find("height").text)

        # Find all the bounding objects
        for label_object in root.findall("object"):
            # Temp array for csv, initialized by the training types
            temp_csv = ["UNASSIGNED"]

            # gs://prefix/name/{image_name}
            cloud_path = f"{path_prefix}/{os.path.splitext(file)[0]}.png"
            temp_csv.append(cloud_path)

            # Class label
            temp_csv.append(label_object.find("name").text)

            # Bounding box coordinate
            bounding_box = label_object.find("bndbox")

            # Add the upper left coordinate
            x_min = float(bounding_box.find("xmin").text) / width
            y_min = float(bounding_box.find("ymin").text) / height
            temp_csv.extend([x_min, y_min])

            # Add the lower left coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Add the lower right coordinate
            x_max = float(bounding_box.find("xmax").text) / width
            y_max = float(bounding_box.find("ymax").text) / height
            temp_csv.extend([x_max, y_max])

            # Add the upper right coordinate (not necessary, left blank)
            temp_csv.extend(["", ""])

            # Append to the res
            temp_res.append(temp_csv)
    return temp_res


if __name__ == "__main__":
    # Add the argument parse
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    arg_p.add_argument("-p", "--bucket_prefix",
                       required=True,
                       type=str,
                       help="google cloud storage bucket name (just the string, no / or .)")

    args = vars(arg_p.parse_args())

    # Prefix of the cloud storage
    ori_prefix = f"gs://{args['bucket_prefix']}/raw"
    # Array for final csv file
    res = xml2csv(args["local_labels_dir"], ori_prefix)

    res_csv = pd.DataFrame(res,
                           columns=["set","path", "label",
                                    "x_min", "y_min",
                                    "x_max", "y_min",
                                    "x_max", "y_max",
                                    "x_min", "y_max"])
    res_csv.to_csv("res2.csv", index=False, header=False)

