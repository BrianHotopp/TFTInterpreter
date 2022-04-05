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
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
class ModelTrainer:
    """
    class to hold information for model training
    """
    def __init__(self, classes_file_path, labels_file_path, images_file_path, verbose=False, batch_size=2, shuffle=False, epochs=10) -> None:
        self.classes = self.get_classes(classes_file_path)
        self.labels_file_path = str(labels_file_path)
        self.images_file_path = str(images_file_path)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.epochs = epochs
        self.verbose = verbose
        self.labels = self.get_labels(labels_file_path)
        self.model = None

    def get_classes(self, classes_file_path):
        """
        classes_file_path: path to a classes file
        """
        classes = {}
        with open(classes_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    line = line.split(',')
                    classes[line[0]] = line[1]
        return classes
    def train(self):
        dataset = Dataset(self.annotations_dir, self.images_dir)
        loader = DataLoader(dataset, self.batch_size, self.shuffle)
        self.model = Model(self.labels)
        self.model.fit(loader, dataset, self.verbose, self.epochs)
    def save_model(self):
        self.model.save(self.model_file_path)

def main():
    arg_p = argparse.ArgumentParser()

    arg_p.add_argument("-l", "--local_labels_dir",
                       required=True,
                       type=str,
                       help="path to directory containing all the xml file labels")
    arg_p.add_argument("-i", "--local_images_dir",
                       required=True,
                       type=str,
                       help="path to directory containing all the images")
    arg_p.add_argument("-s", "--set_file",
                       required=True,
                       type=str,
                       help="path to csv file containing names and abbreviations for the units from the current set")
    args = vars(arg_p.parse_args())
    classes_file_path = Path(args["set_file"])
    annotations_dir = Path(args["local_labels_dir"])
    images_dir = Path(args["local_images_dir"])

    # create model trainer object
    model_trainer = ModelTrainer(classes_file_path, annotations_dir, images_dir)
    # train model
    model_trainer.train()
    # save model
    model_trainer.save_model()


if __name__ == "__main__":
    #test_detecto_working()
    main()