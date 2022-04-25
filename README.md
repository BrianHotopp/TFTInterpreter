# TFTInterpreter

The Teamfight Tactics Interpreter is a continuously running loop that reads a TFT screenshot into a machine-readable format. By taking repeated screenshots of the planning phase of a TFT game, the interpreter represents all present champions. This is supplemented by a recommendation system that reviews the units in play and identifies the strongest available champion synergies to build an effective team.

---

## Installation and use

The TFT Interpreter was written for Python version 3.10, and champion data is up-to-date through TFT patch 12.7

##### Installing the Teamfight Tactics interpreter
```
git clone https://github.com/BrianHotopp/TFTInterpreter
```
##### Installing all module dependencies
```
pip install -r requirements.txt
```
##### Creating training data

Create the 'data' and 'models' directories in your local TFTInterpreter directory. 

Run src/preprocessing/gather_data/auto_screenshotter.py or src/preprocessing/gather_data/manual_screenshotter.py to create screenshots, save them to the data/images folder.

Create annotations for each image using the [labelImg](https://github.com/tzutalin/labelImg) tool, and store annotations in the data/annotations folder.

Create a model file by running src/preprocessing/train_model/ModelTrainer.py, this will create a .pth file that should be saved to the models directory (an example model file is models/10epoch.pth).
