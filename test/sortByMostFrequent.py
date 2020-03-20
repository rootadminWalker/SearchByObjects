#!/usr/bin/env python3

from os import path, listdir
import cv2 as cv
from operator import itemgetter

from core.Detection import YOLOPreprocessWithTarget, YOLODetect, yoloIMG
from core.basePaths import basePaths
from core.settings import Settings
from time import time

# Initialize start time
start = time()

# Initialize variables
yolo = YOLODetect(
    model_path=basePaths(
        '../models/yolov3_416.h5'
    ).joinBase(),
    anchors_path=basePaths(
        '../models/yolo_anchors.txt'
    ).joinBase(),
    classes_path=basePaths(
        '../models/coco_classes.txt'
    ).joinBase()
)

target = 'cow'
videos = basePaths(
    '../static/videos'
).joinBase()

_targetCount = 0
_allCounts = {}

# You can set how much themes will the program
# Jump to predict. More themes jumped will resulting
# In a faster program and fewer themes jumped will be Slow
#
# Total frames you wanna jump = total seconds * fps
_jumpThemes = 500

# Start looping with all videos
for video in listdir(videos):
    boxes = {}
    video_name = path.join(videos, video)  # Read the video
    video = cv.VideoCapture(video_name)

    # Configure the settings
    settings = Settings(video)
    start_predict = 0
    while True:
        ret, frame = video.read()
        if not ret:
            continue

        # We'll jump n themes before we predict
        # In this case, we jumped 100 themes
        if start_predict % _jumpThemes == 0:
            frame = yoloIMG(frame).preprocess_to()  # Preprocess the frame into PIL format

            frame, box_count, predicted_classes = yolo.detect(frame)  # Predict our frame

            frame = yoloIMG(frame).rollback()  # Rollback our theme

            # Get duration in H:M:S format
            duration = settings.get_current_SEC()
            settings.format_to_HMS(duration)
            duration = settings.duration

            # Process our output with target counting
            result = YOLOPreprocessWithTarget(
                [predicted_classes, box_count], duration,
                target
            ).process_outputs()
            targetCount = result[duration]['target']

            print(video_name + ":", duration, predicted_classes, box_count, targetCount, end='\r')

            _targetCount += targetCount

        start_predict += 1

        # Check if we have to stop
        if settings.get_fps() * settings.get_current_SEC() == settings.get_frames_count():
            break

    _allCounts[video_name] = _targetCount

# Sort our targets from largest to smallest
_allCounts = sorted(_allCounts.items(), key=itemgetter(1), reverse=True)
_allCounts = dict((key, value) for key, value in _allCounts)
print(_allCounts)

# Initialize end time
end = time()

print("Program runtime: {}".format(
    round(
        end - start, 5
    )
))
