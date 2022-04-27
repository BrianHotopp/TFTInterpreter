import detecto
import detecto.core
import cv2
import torchvision.ops as ops
import numpy as np
from pathlib import Path
class Predictor:
    """
    This class predicts the units on the image.
    """
    # load static resources from disk on initialization
    carousel_image_path = Path("src/tftinterpreter/predictor/static/carousel.png")
    gray_helmet_path = Path("src/tftinterpreter/predictor/static/gray_helmet.png")
    blue_helmet_path = Path("src/tftinterpreter/predictor/static/blue_helmet.png")
    augment_button_path = Path("src/tftinterpreter/predictor/static/augment_button.png")
    enemy_bench_empty_path = Path("src/tftinterpreter/predictor/static/empty_bench.png")
    carousel_image = cv2.imread(str(carousel_image_path))
    gray_helmet_image = cv2.imread(str(gray_helmet_path))
    blue_helmet_image = cv2.imread(str(blue_helmet_path))
    augment_button_image = cv2.imread(str(augment_button_path))
    enemy_bench_empty_image = cv2.imread(str(enemy_bench_empty_path))

    def __init__(self, labels_file_path: str, model_file_path: str) -> None:
        """
        Initialize a predictor object.
        Args:
            self: the current Predictor object
            labels_file_path: path to a labels file
            model_path: path to a model file
        """
        self._labels = self.get_labels(labels_file_path)
        self._model = detecto.core.Model.load(model_file_path, list(self._labels.values()))
        # dict giving an id to a unit
        self.label_idx = {v: k for k, v in enumerate(self._labels.values())}

    @staticmethod
    def get_labels(labels_file_name) -> dict:
        """
        Get the labels of the set 6 units.
        Args:
            self: the current Predictor object
            labels_file_name: the filename to read from
        Returns:
            dictionary of set 6 units parsed
        """
        # read set 6 units in
        SET_6_UNITS = dict()
        with open(labels_file_name) as classes_file_handle:
            for line in classes_file_handle.readlines():
                unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
                SET_6_UNITS[unit_name] = abbreviated_name
        return SET_6_UNITS

    def predict_on_image(self, image):
        """
        Predict unit(s) given image object.
        Args:
            self: the current Predictor object
            image: 1920x1080 RGB PIL image to predict on
        Returns:
            labels: list[str] representing the units on the board
                    makes a prediction of units on the board using a screenshot
            scores: the confidence score
        """
        img = np.array(image)
        labels, boxes, scores = self._model.predict(img)
        # perform hard non-max suppression using pytorch
        kept = ops.nms(boxes, scores, 0.5)
        boxes = boxes[kept]
        labels = [labels[i] for i in kept]
        scores = scores[kept]
        return labels, boxes, scores

    def predict_on_image_file(self, image_path, show_image_popup=False):
        """
        Predict unit(s) given an image file.
        Args:
            self: the current Predictor object
            image_path: str path to the image to predict on
            show_image_popup: boolean for whether or not to pop out the image
        Returns:
            labels: list[str] representing the units on the board
                    makes a prediction of units on the board using a screenshot
            boxes: the box locations on the image
            scores: the confidence score
        """
        img = detecto.utils.read_image(image_path)
        labels, boxes, scores = self._model.predict(img)

        if show_image_popup:
            detecto.visualize.show_labeled_image(img, boxes, labels)
        return labels, boxes, scores

    @classmethod
    def PILtoCV2(img):
        """
        Convert an image in PIL form to cv2.
        Args:
            img: image object
        Returns:
            open_cv_image converted
        """
        npimg = np.array(img)
        # Convert RGB to BGR
        open_cv_image = npimg[:, :, ::-1].copy()
        return open_cv_image

    @classmethod
    def image_in_image(self, image1, image2, threshold = 0.8):
        """
        Determine if an image is in another image.
        Args:
            self: the current Predictor object
            image1: image in cv2
            image2: image in cv2
            threshold: threshold for finding an image
        Returns:
            boolean: true if image1 is in image2
        """
        res = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
        flag = False
        if np.amax(res) > threshold:
            flag = True
        return flag

    @classmethod
    def in_planning_phase(screenshot):
        """
        Determine whether the player is in the planning phase.
        Args:
            screenshot: PIL Image
        Returns:
            boolean: whether or not the user is in the planning phase
        """
        screenshot = Predictor.PILtoCV2(screenshot)
        in_carousel = Predictor.image_in_image(Predictor.carousel_image, screenshot)
        gray_helmet = Predictor.image_in_image(Predictor.gray_helmet_image, screenshot, threshold=0.4)
        blue_helmet = Predictor.image_in_image(Predictor.blue_helmet_image, screenshot, threshold=0.5)
        augment_button = Predictor.image_in_image(Predictor.augment_button_image, screenshot)
        enemy_bench_empty = Predictor.image_in_image(Predictor.enemy_bench_empty_image, screenshot)
        """
        Test print statements:
            print(f"carou{in_carousel}")
            print(f"gh{gray_helmet}")
            print(f"bh{blue_helmet}")
            print(f"ab{augment_button}")
            print(f"enemb{enemy_bench_empty}")
            print(f"am in planning{planning}")
        """
        planning = (blue_helmet or gray_helmet) and (not in_carousel) and (not augment_button) and (enemy_bench_empty)
        return planning
