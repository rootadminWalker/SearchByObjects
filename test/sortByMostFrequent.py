#!/usr/bin/env python3

from os import path, listdir
import cv2 as cv
from operator import itemgetter

from core.Detection import YOLOPreprocessWithTarget, YOLODetect, yoloIMG
from core.basePaths import basePaths
from core.settings import Settings

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
audios = basePaths(
    '../static/audios'
).joinBase()

_targetCount = 0
_allCounts = {}

for video in listdir(audios):
    boxes = {}
    video_name = basePaths(
        path.join(audios, video)
    ).joinBase()
    video = cv.VideoCapture(video_name)

    settings = Settings(video)
    start_predict = 0
    while True:
        ret, frame = video.read()
        if not ret:
            continue

        if start_predict % 100 == 0:
            frame = yoloIMG(frame).preprocess_to()

            frame, box_count, predicted_classes = yolo.detect(frame)

            frame = yoloIMG(frame).rollback()

            duration = settings.get_current_SEC()
            settings.format_to_HMS(duration)
            duration = settings.duration

            _, targetCount = YOLOPreprocessWithTarget(
                [predicted_classes, box_count], duration,
                target
            ).process_outputs()
            print(video_name + ":", duration, predicted_classes, box_count, targetCount, end='\r')

            _targetCount += targetCount

        start_predict += 1

        if settings.get_fps() * settings.get_current_SEC() == settings.get_frames_count():
            break

    _allCounts[video_name] = _targetCount

_allCounts = sorted(_allCounts.items(), key=itemgetter(1), reverse=True)
_allCounts = dict((key, value) for key, value in _allCounts)
