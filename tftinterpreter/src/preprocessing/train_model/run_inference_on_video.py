#!python

# System Imports
import argparse

# Third Party Imports
import cv2
import torch
import detecto
from detecto.visualize import detect_video
from detecto.utils import normalize_transform
from detecto.core import Dataset, DataLoader, Model
import torchvision.ops.boxes as bops
from torchvision import transforms

def custom_make_prediction(model, img) -> tuple(list, list, list):
    """
    Make a custom prediction.
    Args:
        model: the model
        img: image to make prediction on
    """
    labels, boxes, scores = model.predict(img)
    all_preds = filter(lambda x: x[2] > 0.2, zip(labels, boxes, scores))
    best = []
    thresh = 0
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
            cur_bbox = torch.reshape(b[0],(1, 4))
            if bops.box_iou(cur_bbox, bbox) > thresh:
                b[1].append((p[0], p[2]))
                found_in_best = 1
                break
        if not found_in_best:
            best.append((bbox, [(label, conf)]))
    best = [(x[0], max(x[1], key=lambda z: z[1])) for x in best]
    if len(best) == 0:
        labels = ()
        boxes = []
        scores = []
    else:
        boxes, labelsandscores = zip(*best)
        labels, scores = zip(*labelsandscores)
        boxes = [torch.reshape(x, (4,)) for x in boxes]
        boxes = torch.stack(boxes)
    return labels, boxes, scores

# command to run:
# 
# there is a bug in detecto that I monkey patched according to a github issue LOL
"""
https://github.com/alankbi/detecto/issues/106
"""
def detect_video(model: detecto.core.Model, input_file: str, output_file: str, \
                    fps: int=30, score_filter: float=0.6) -> None:
    """
    Takes in a video and produces an output video with object detection
    run on it (i.e. displays boxes around detected objects in real-time).
    Output videos should have the .avi file extension. Note: some apps,
    such as macOS's QuickTime Player, have difficulty viewing these
    output videos. It's recommended that you download and use
    `VLC <https://www.videolan.org/vlc/index.html>`_ if this occurs.

    Args:
        model: The trained model with which to run object detection.
        input_file: The path to the input video.
        output_file: The name of the output file. Should have a .avi file extension.
        fps: (Optional) Frames per second of the output video. Defaults to 30.
        score_filter: (Optional) Minimum score required to show a prediction. Defaults to 0.6.

    **Example**:
        >>> from detecto.core import Model
        >>> from detecto.visualize import detect_video
        >>> model = Model.load('model_weights.pth', ['tick', 'gate'])
        >>> detect_video(model, 'input_vid.mp4', 'output_vid.avi', score_filter=0.7)
    """

    # Read in the video
    video = cv2.VideoCapture(input_file)
    print(video)
    # Video frame dimensions
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Scale down frames when passing into model for faster speeds
    scaled_size = 800
    scale_down_factor = min(frame_height, frame_width) / scaled_size

    # The VideoWriter with which we'll write our video with the boxes and labels
    # Parameters: filename, fourcc, fps, frame_size
    print(frame_width, frame_height)
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), fps, (frame_width, frame_height))

    # Transform to apply on individual frames of the video
    transform_frame = transforms.Compose([  # TODO Issue #16
        transforms.ToPILImage(),
        transforms.Resize(scaled_size),
        transforms.ToTensor(),
        normalize_transform(),
    ])

    # Loop through every frame of the video
    while True:
        ret, frame = video.read()
        # Stop the loop when we're done with the video
        if not ret:
            break

        # The transformed frame is what we'll feed into our model
        transformed_frame = transform_frame(frame)
        transformed_frame = frame  # TODO: Issue #16
        predictions = custom_make_prediction(model, transformed_frame)

        # Add the top prediction of each class to the frame
        for label, box, score in zip(*predictions):
            # Since the predictions are for scaled down frames,
            # we need to increase the box dimensions
            # box *= scale_down_factor  # TODO Issue #16

            # Create the box around each object detected
            # Parameters: frame, (start_x, start_y), (end_x, end_y), (r, g, b), thickness
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 3)

            # Write the label and score for the boxes
            # Parameters: frame, text, (start_x, start_y), font, font scale, (r, g, b), thickness
            cv2.putText(frame, '{}: {}'.format(label, round(score.item(), 2)), (int(box[0]), int(box[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        # Write this frame to our video file
        out.write(frame)

        # If the 'q' key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # When finished, release the video capture and writer objects
    video.release()
    out.release()

    # Close all the frames
    cv2.destroyAllWindows()

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
        input_video_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\demo_videos\\2022-03-04 14-04-31.mkv" 
        output_video_path = "E:\Dropbox\Spring 2022\Software Design and Documentation\datadump\TFTInterpreterData\demo_videos\\long(inference).mkv"

        detect_video(model, input_video_path, output_video_path, score_filter = 0.5, fps=30)
        #detect_live(model, score_filter=0.5)
       
    else:
        model = Model(labels)
        model.fit(loader, dataset, verbose=True, epochs=10)
        print("saving model")
        model.save(model_save_path)