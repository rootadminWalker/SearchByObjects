#!/usr/bin/env python3

from core.settings import Settings

import os
import cv2 as cv

videos = '../static/videos'
_smallest = 0
_targetTimes = 33

_all = os.listdir(videos)

for video in _all:
    vid = cv.VideoCapture(
        os.path.join(videos, video)
    )
    setting = Settings(vid)
    frames = setting.get_frames_count()
    if _smallest > frames or _smallest == 0:
        _smallest = frames

print(_smallest // _targetTimes)
