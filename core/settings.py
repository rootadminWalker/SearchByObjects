#!/usr/bin/env python3

"""
MIT License

Copyright (c) 2020 rootadminWalker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import cv2 as cv

"""
    This class configure the settings of your video
"""

class Settings:
    def __init__(self, video: cv.VideoCapture):
        """
        Constructor

        :param video: Your video
        """

        self.video = video
        self.duration = ""
        self.fps = self.get_fps()
        self.time_length = self.get_total_SEC()

    def get_total_SEC(self) -> float:
        """
        Get video total duration in SECONDS

        :return: seconds in float format
        """
        return self.get_frames_count() / self.get_fps()

    def get_total_MSEC(self) -> float:
        """
        Get video total duration in MILLISECONDS

        :return: milliseconds in float format
        """
        return self.video.get(cv.CAP_PROP_POS_MSEC)

    def get_fps(self) -> int:
        """
        Get fps of the video

        :return: Video fps
        """
        return self.video.get(cv.CAP_PROP_FPS)

    def get_current_SEC(self) -> float:
        """
        Get the current duration of the video

        :return:
        """
        return self.video.get(cv.CAP_PROP_POS_MSEC) / 1000

    def get_frames_count(self) -> int:
        """
        Get video total frames count

        :return: Video total frames count
        """
        return self.video.get(cv.CAP_PROP_FRAME_COUNT)

    def format_to_HMS(self, duration: float):
        """
        Format total duration into H:M:S format

        :param duration: The duration
        """

        all_idxes = []
        hour = int(duration // 3600)
        left = duration % 3600

        minute = int(left // 60)
        left = left % 60

        seconds = int(left)

        tmp = list(map(str, [hour, minute, seconds]))
        for elem in range(len(tmp)):
            _behind = tmp[elem-1] if elem != 0 else '0'
            _current = tmp[elem]
            if tmp != ['0', '0', '0']:
                if tmp[0] == '0':
                    if (_behind == '0') and (_current == '0'):
                        all_idxes.append(0)

        [tmp.pop(idx) for idx in all_idxes]
        self.duration = ':'.join(tmp)


if __name__ == '__main__':
    video = cv.VideoCapture('../../audios/test.mp4')
    s = Settings(video)
    s.format_to_HMS(2)
    print(s.duration)
