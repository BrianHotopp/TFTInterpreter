import time
import detecto
import cv2
import os
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
        # load static resources from disk on initialization
        carousel_image_path = "../gather_data/resources/augmentbutton.PNG"
        gray_helmet_path = "../gather_data/resources/helmet.PNG"
        blue_helmet_path = "../gather_data/resources/helmetblue.PNG"
        augment_button_path = "../gather_data/resources/augmentbutton.PNG"
        enemy_bench_empty_path = "../gather_data/resources/emptybench.PNG"
        self.carousel_image = cv2.imread(carousel_image_path)
        self.gray_helmet_image = cv2.imread(gray_helmet_path)
        self.blue_helmet_image = cv2.imread(blue_helmet_path)
        self.augment_button_image = cv2.imread(augment_button_path)
        self.enemy_bench_empty_image = cv2.imread(enemy_bench_empty_path)

    def PILtoCV2(self, img):
        """
        converts an image in PIL form to cv2
        """
        npimg = np.array(img)
        # Convert RGB to BGR
        open_cv_image = npimg[:, :, ::-1].copy()
        return open_cv_image
    def image_in_image(self, image1, image2, threshold = 0.8):
        """
        image1: image in cv2
        image2: image in cv2
        returns true if image1 is in image2
        """
        res = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
        flag = False
        if np.amax(res) > threshold:
            flag = True
        return flag

    def in_planning_phase(self, screenshot):
        """
        image: PIL Screenshot
        """
        screenshot = self.PILtoCV2(screenshot)
        in_carousel = self.image_in_image(self.carousel_image, screenshot)
        gray_helmet = self.image_in_image(self.gray_helmet_image, screenshot, threshold=0.4)
        blue_helmet = self.image_in_image(self.blue_helmet_image, screenshot, threshold=0.5)
        augment_button = self.image_in_image(self.augment_button_image, screenshot)
        enemy_bench_empty = self.image_in_image(self.enemy_bench_empty_image, screenshot)
        """
        print(f"carou{in_carousel}")
        print(f"gh{gray_helmet}")
        print(f"bh{blue_helmet}")
        print(f"ab{augment_button}")
        print(f"enemb{enemy_bench_empty}")
        print(f"am in planning{planning}")
        """
        planning = (blue_helmet or gray_helmet) and (not in_carousel) and (not augment_button) and (enemy_bench_empty)
        return planning
    def get_labels(self, labels_file_name):
        # read set 6 units in
        SET_6_UNITS = dict()
        with open(labels_file_name) as classes_file_handle:
            for line in classes_file_handle.readlines():
                unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
                SET_6_UNITS[unit_name] = abbreviated_name
        return SET_6_UNITS

    def reduce_prediction(self, labels, boxes, scores):
        all_preds = filter(lambda x: x[2] > 0.2, zip(labels, boxes, scores))
        best = []
        thresh = 0.1
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
        return labels, boxes, scores

    def predict_on_image(self, image):
        """
        image: 1920x1080 RGB PIL image to predict on
        """
        img = np.array(image)
        labels, boxes, scores = self.reduce_prediction(*self._model.predict(img))
        return labels, scores

    def predict_on_image_file(self, image_path, show_image_popup=False):
        """
        Params:
        image_path: str path to the image to predict on
        Returns:
        labels: list[str] representing the units on the board
        makes a prediction of units on the board using a screenshot
        """
        img = utils.read_image(image_path)
        labels, boxes, scores = self._model.predict(img)

        if show_image_popup:
            show_labeled_image(img, boxes, labels)
        return labels, boxes, scores
