#!/usr/bin/env python3

from core.Detection import YOLODetect, yoloIMG
from core.basePaths import basePaths

import cv2 as cv

filepath = '../static/bgs/20200120_150626.jpg'
img = cv.imread(filepath, cv.IMREAD_COLOR)

result_json = open(
    basePaths('./result.json').joinBase(), 'w+'
)
boxes = {}

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

frame = yoloIMG(img).preprocess_to()

frame, box_count, predicted_classes = yolo.detect(frame)

frame = yoloIMG(frame).rollback()

cv.imshow('frame', frame)
key = cv.waitKey(0)
cv.imwrite(filepath, frame)
