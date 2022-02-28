import shutil
import os
import argparse
import codecs

def check():
    # To parse the xml files
    import xml.etree.ElementTree as ET
    annotation_dir = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\annotations"
    images_dir = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw"
    j = [str(x) for x in list(range(0, 298))]
    j.sort()

    annotations_list = os.listdir(annotation_dir)
    images_list = os.listdir(images_dir)

    for i in range(len(images_list)):
        # Check the file name ends with xml
        annotation_filename = annotations_list[i]
        image_filename = images_list[i]
        if not annotation_filename.endswith(".xml"):
            continue
        print(annotation_filename)
        correct_annotation_name = f"{j[i]}.xml"
        correct_image_name = f"{j[i]}.png"

        print(correct_annotation_name)
        print(correct_image_name)
        assert(annotation_filename== correct_annotation_name)
        assert(image_filename == correct_image_name)
        i+=1

        
if __name__ == "__main__":
    # Add the argument parse
    check()
