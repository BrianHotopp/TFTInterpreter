#!python

# System Imports
import argparse

# Third Party Imports
from detecto.visualize import detect_live
from detecto.core import Dataset, DataLoader, Model

if __name__ == "__main__":
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
        model_load_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model.load(model_load_path, labels)
        detect_live(model, score_filter=0.5)
       
    else:
        model_save_path =  "E:\Dropbox\Spring 2022\Software Design and Documentation\code\models\\10epoch.pth"
        model = Model(labels)
        model.fit(loader, dataset, verbose=True, epochs=10)
        print("saving model")
        model.save(model_save_path)
