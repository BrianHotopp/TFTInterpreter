#!python

# Third Party Imports
from pathlib import Path

# Local Imports
from src.preprocessing.train_model.ModelTrainer import ModelTrainer

class TestClass:
    """
    Test class.
    """
    def test_initialization(self) -> None:
        """
        Test the intialization of the model.
        """
        cl_fp = Path("preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        assert(isinstance(mt, ModelTrainer))

    def test_get_classes(self) -> None:
        """
        Test reading classes from csv.
        """
        classes = ModelTrainer.get_classes(Path("preprocessing/train_model/test_resources/test_set_classes.csv")) 
        assert(len(classes) == 4)
        assert(classes["Singed"] == "sing")
        assert(classes["Twitch"] == "twit")
        assert(classes["Warwick"] == "warw")
        assert(classes["Tryndamere"] == "tryn")

    def test_train(self) -> None:
        """
        Test the training of the model.
        """
        cl_fp = Path("preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        mt.train()
        assert(mt.model is not None)

    def test_save(self) -> None:
        """
        Test saving the model.
        """
        cl_fp = Path("preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        mt.train()
        sp = Path("preprocessing/train_model/test_resources/models/test_model.pth")
        mt.save_model(sp)
        assert(sp.exists())
