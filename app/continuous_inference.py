import time
import detecto
import os
import torch
import argparse
from detecto import utils
from detecto.visualize import show_labeled_image
from detecto.core import Dataset, DataLoader, Model
import matplotlib.pyplot as plt
import torchvision.ops.boxes as bops



import numpy as np
import matplotlib.pyplot as plt
#def get_best(labels, boxes, scores):
def custom_make_prediction(model, image_path):
    start = time.time()
    img = utils.read_image(image_path)
    labels, boxes, scores = model.predict(img)
    all_preds = filter(lambda x: x[2] > 0.2, zip(labels, boxes, scores))
    best = []
    thresh = 0.4
    found_in_best = 0
    # for each prediction
    # check if there is a similar bounding box in best
    # if there is, add the current prediction to that bounding box
    # if there isn't, add the current bounding box: label, confidence to the list
    for p in all_preds:
        found_in_best = 0
        label = p[0]
        bbox = p[1]
        conf = p[2]
        bbox = torch.reshape(bbox, (1, 4))
        for b in best:
            cur_bbox = torch.reshape(b[0],(1, 4))
            if bops.box_iou(cur_bbox, bbox) > thresh:
                b[1].append((p[0], p[2]))
                found_in_best = 1
                break
        if not found_in_best:
            best.append((bbox, [(label, conf)]))
    best = [(x[0], max(x[1], key=lambda z: z[1])) for x in best]
    boxes, labelsandscores = zip(*best)
    labels, scores = zip(*labelsandscores)
    for i in boxes:
        print(i)
    boxes = [torch.reshape(x, (4,)) for x in boxes]
    boxes = torch.stack(boxes)
    end = time.time()
    print(f"Prediction took {end-start} seconds")
    print(labels)
    labels = [labels[i]+"{:.2f}".format(scores[i]) for i in range(len(labels))]
    show_labeled_image(img, boxes, labels)
    return labels, boxes, scores 

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
        model_load_path = "code/models/10epoch.pth"
        #model_load_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model.load(model_load_path, labels)
        #test_image_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\\raw\\1.png"
        test_image_path = "datadump/TFTInterpreterData/raw/1000.png"
        custom_make_prediction(model, test_image_path)

    else:
        model_save_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model(labels)
        model.fit(loader, dataset, verbose=True, epochs=10)
        print("saving model")
        model.save(model_save_path)
if __name__ == "__main__":
    #test_detecto_working()
    main()