#!python

# System Imports
import argparse

# Third Party Imports
from detecto.core import Dataset, DataLoader, Model
from pathlib import Path

class ModelTrainer:
    """
    This class holds information for model training.
    """
    def __init__(self, classes_file_path, annotation_dir, images_dir, verbose=False, batch_size=2, shuffle=False, epochs=10) -> None:
        """
        Initialize a ModelTrainer object.
        Args:
            classes_file_path: path to the classes
            annotation_dir: directory of the annotations
            images_dir: directory of the images
            verbose: boolean to print
            batch_size: size of the batch
            shuffle: whether or not to shuffle the data
            epochs: number of epochs
        """
        self.classes = self.get_classes(classes_file_path)
        self.annotations_dir = str(annotation_dir)
        self.images_dir = str(images_dir)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.epochs = epochs
        self.verbose = verbose
        self.model = None

    @staticmethod
    def get_classes(classes_file_path: Path) -> dict:
        """
        Gets the classes from the file to a dictionary.
        Args:
            classes_file_path: path to a classes file
        Returns:
            dictionary of classes
        """
        classes = {}
        with open(classes_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    line = line.split(',')
                    classes[line[0].strip()] = line[1].strip()
        return classes

    def train(self) -> None:
        """
        Train the model.
        """
        dataset = Dataset(self.annotations_dir, self.images_dir)
        loader = DataLoader(dataset, batch_size = self.batch_size, shuffle = self.shuffle)
        self.model = Model(list(self.classes.values()))
        self.model.fit(loader, dataset, self.verbose, self.epochs)

    def save_model(self, save_path) -> None:
        """
        Save model to disk.
        Args:
            save_path: python pathlib object to save model to
        """
        self.model.save(str(save_path))

if __name__ == "__main__":
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
