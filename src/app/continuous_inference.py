#!python

# Third Party Imports
import torch
from detecto import utils
from detecto.visualize import show_labeled_image
from detecto.core import Model
import torchvision.ops.boxes as bops
import numpy as np
import matplotlib.pyplot as plt
import PIL

class Predictor:
    """
    This class predicts the units on the image.
    """
    def __init__(self, labels_file_path: str, model_file_path: str) -> None:
        """
        Initializae a predictor object.
        Args:
            self: the current Predictor object
            labels_file_path: path to a labels file
            model_path: path to a model file
        """
        self._labels = self.get_labels(labels_file_path)
        self._model = Model.load(model_file_path, list(self._labels.values()))

    def get_labels(self, labels_file_name: str) -> dict():
        """
        Get the labels for the units.
        Args:
            self: the current Predictor object
            labels_file_name: path to a labels file name
        Returns:
            dictionary of the set 6 units
        """
        # read set 6 units in
        SET_6_UNITS = dict()
        with open(labels_file_name) as classes_file_handle:
            for line in classes_file_handle.readlines():
                unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
                SET_6_UNITS[unit_name] = abbreviated_name
        return SET_6_UNITS

    def predict_on_image(self, image: PIL.Image.Image) -> tuple:
        """
        Predicts the units on the image.
        Args:
            image: 1920x1080 RGB PIL image to predict on
        Returns:
            labels of the units and the confidence score
        """
        img = np.array(image)
        labels, _, scores = self._model.predict(img)
        return labels, scores

    def predict_on_image_file(self, image_path: str, show_image_popup: bool=False) -> list:
        """
        Predicts the units given a screenshot.
        Args:
            image_path: str path to the image to predict on
        Returns:
            labels: list[str] representing the units on the board
                    makes a prediction of units on the board using a screenshot
        """
        img = utils.read_image(image_path)
        labels, boxes, scores = self._model.predict(img)
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
                cur_bbox = torch.reshape(b[0], (1, 4))
                if bops.box_iou(cur_bbox, bbox) > thresh:
                    b[1].append((p[0], p[2]))
                    found_in_best = 1
                    break
            if not found_in_best:
                best.append((bbox, [(label, conf)]))
        best = [(x[0], max(x[1], key=lambda z: z[1])) for x in best]
        boxes, labelsandscores = zip(*best)
        labels, scores = zip(*labelsandscores)
        boxes = [torch.reshape(x, (4,)) for x in boxes]
        boxes = torch.stack(boxes)
        labels = [labels[i] + "{:.2f}".format(scores[i]) for i in range(len(labels))]
        if show_image_popup:
            show_labeled_image(img, boxes, labels)
        return labels, boxes, scores
