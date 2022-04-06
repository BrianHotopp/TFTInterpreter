from PIL import Image
from src.app.continuous_inference import Predictor
from pathlib import Path


class TestClass:
    def test_in_planning_phase(self):
        im0p = Path("test/app/test_resources/0.png")
        with Image.open(im0p) as im0:
            assert(Predictor.in_planning_phase(im0))
        im1p = Path("test/app/test_resources/1.png")
        with Image.open(im1p) as im1:
            assert(Predictor.in_planning_phase(im1))
        im2p = Path("test/app/test_resources/2.png")
        with Image.open(im2p) as im2:
            assert(Predictor.in_planning_phase(im2))
        im3p = Path("test/app/test_resources/3.png")
        with Image.open(im3p) as im3:
            assert(not Predictor.in_planning_phase(im3))



       