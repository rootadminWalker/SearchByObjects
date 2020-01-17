#!/usr/bin/env python3

from core.basePaths import basePaths
from core.COCO_classes_tag import *
from core.Detection import YOLOPreprocess, YOLODetect, yoloIMG
from core.Factory import Factory
from core.settings import Settings

import cv2 as cv
import os

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

boxesFromAll = []

for video in os.listdir(audios):
    boxes = {}
    video = cv.VideoCapture(video)
    settings = Settings(video)
    start_predict = 0
    for _ in range(settings.get_fps()):
        ret, frame = video.read()

        if start_predict % 100 == 0:
            pass

        start_predict += 1
