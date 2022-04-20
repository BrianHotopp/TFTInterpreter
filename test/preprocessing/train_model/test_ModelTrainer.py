from src.preprocessing.train_model.ModelTrainer import ModelTrainer
from pathlib import Path
class TestClass:
    def test_initialization(self):
        cl_fp = Path("test/preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("test/preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("test/preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        assert(isinstance(mt, ModelTrainer))
    def test_get_classes(self):
        """
        test reading classes from csv
        """
        classes = ModelTrainer.get_classes(Path("test/preprocessing/train_model/test_resources/test_set_classes.csv")) 
        assert(len(classes) == 4)
        assert(classes["Singed"] == "sing")
        assert(classes["Twitch"] == "twit")
        assert(classes["Warwick"] == "warw")
        assert(classes["Tryndamere"] == "tryn")
    def test_train(self):
        cl_fp = Path("test/preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("test/preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("test/preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        mt.train()
        assert(mt.model is not None)
    def test_save(self):
        cl_fp = Path("test/preprocessing/train_model/test_resources/test_set_classes.csv")
        im_fp = Path("test/preprocessing/train_model/test_resources/raw_images")
        lab_fp = Path("test/preprocessing/train_model/test_resources/raw_images_labels")
        mt = ModelTrainer(cl_fp, im_fp, lab_fp)
        mt.train()
        sp = Path("test/preprocessing/train_model/test_resources/models/test_model.pth")
        mt.save_model(sp)
        assert(sp.exists())