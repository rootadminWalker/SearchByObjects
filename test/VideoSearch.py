#!/usr/bin/env python3

import cv2 as cv
import json
from core import Settings
from core.Detection import YOLODetect, YOLOPreprocess, yoloIMG
from core.basePaths import basePaths

video = cv.VideoCapture(
    basePaths('../static/audios/test.mp4').joinBase()
)

result_json = open(
    basePaths('./result.json').joinBase(), 'w+'
)
boxes = {}

setting = Settings(video)
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

time_length = setting.get_total_SEC()
start_predict = 0

while True:
    ret, frame = video.read()
    if not ret:
        continue

    if start_predict % 100 == 0:
        frame = yoloIMG(frame).preprocess_to()

        frame, box_count, predicted_classes = yolo.detect(frame)

        frame = yoloIMG(frame).rollback()

        duration = setting.get_current_SEC()
        setting.format_to_HMS(duration)
        duration = setting.duration

        perFrame_classes = YOLOPreprocess(
            [predicted_classes, box_count], duration
        ).process_outputs()

        boxes.update(perFrame_classes)

    # cv.imshow('frame', frame)
    # key = cv.waitKey(1)
    #
    # if key in [ord('q'), 27]:
    #     break

    if video.get(cv.CAP_PROP_POS_MSEC) / 1000 >= time_length:
        break

    start_predict += 1

video.release()
cv.destroyAllWindows()
print(boxes)

json.dump(boxes, result_json, indent=4, sort_keys=True)
