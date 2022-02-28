import time
import detecto
import os
import torch
import argparse
from detecto import utils
from detecto.visualize import show_labeled_image
from detecto.core import Dataset, DataLoader, Model
import matplotlib.pyplot as plt

def main():
    arg_p = argparse.ArgumentParser()

    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the xml file labels")
    arg_p.add_argument("-i", "--local_images_dir",
                       required=True,
                       type=str,
                       help="path to parent directory containing all the images")
    arg_p.add_argument("-s", "--set_file",
                       required=True,
                       type=str,
                       help="csv file containing names and abbreviations for the units from the current set")
               
    args = vars(arg_p.parse_args())
    # read set 6 units in 
    SET_6_UNITS = dict()
    with open(args["set_file"]) as classes_file_handle:
        for line in classes_file_handle.readlines():
            unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
            SET_6_UNITS[unit_name] = abbreviated_name

    annotations_dir = args["local_labels_dir"]
    images_dir = args["local_images_dir"]
    dataset = Dataset(annotations_dir, images_dir)
    loader = DataLoader(dataset, batch_size=2, shuffle=False)
    labels = list(SET_6_UNITS.values())
    load_model = True 
    if load_model:
        model_load_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model.load(model_load_path, labels)
        #test_image_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\faketest\\158.png"
        test_image_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\\1.png"
        img = utils.read_image(test_image_path)
        start = time.time()
        labels, boxes, scores = model.predict(img)
        end = time.time()
        print(f"Prediction took {end-start} seconds")
        print(boxes)
        all_preds = [x for x in zip(labels, boxes, scores) if x[2] > 0.5]
        labels, boxes, scores = zip(*all_preds)
        boxes = [list(x) for x in boxes]
        boxes = torch.tensor(boxes)
        print(labels, boxes, scores)
        print(scores)
        show_labeled_image(img, boxes, labels)

    else:
        model_save_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model(labels)
        model.fit(loader, dataset, verbose=True, epochs=10)
        print("saving model")
        model.save(model_save_path)
if __name__ == "__main__":
    #test_detecto_working()
    main()