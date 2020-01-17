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

from keras_yolo3_qqwweee.yolo import YOLO
from PIL import Image
from core.base_classes import *
from core.Factory import Factory
from core.basePaths import basePaths

class yoloIMG(Img):
    def __init__(self, frame: np.array):
        """
        Inherited by the Img class,
        This class will preprocess the frame
        for our YOLO python wrapper

        :param frame: Your frame
        """
        super(yoloIMG, self).__init__(frame)

    def preprocess_to(self) -> Image:
        """
        Preprocess the image to PIL format

        :return: Your PIL image
        """

        self.img = Image.fromarray(self.img)
        return self.img

    def rollback(self) -> np.array:
        """
        Undo the preprocess

        :return: A rollback image
        """

        self.img = np.array(np.asarray(self.img))
        return self.img


class YOLODetect(Detection):
    def __init__(self, model_path, anchors_path: str, classes_path):
        """
        Inherited by the Detection class, This will
        detect your image using YOLO

        :param model_path: Your YOLO model path
        :param anchors_path: Anchors for your YOLO
        :param classes_path: Your trained labels
        """

        super(YOLODetect, self).__init__(model_path, classes_path)
        self.anchors_path = anchors_path

        self.model = YOLO(
            model_path=self.model_path,
            anchors_path=self.anchors_path,
            classes_path=self.classes_path
        )
        self.frame, self.box_count, self.predicted_classes = None, None, None

    def detect(self, frame: Image) -> (Image, int, list):
        """
        Predict image with YOLO

        :param frame: THe image you want to predict
        :return: frame: your image with drown boxes
                 box_count: The total count of bounding boxes
                 predicted_classes: All predicted classes
        """

        self.frame, self.box_count, self.predicted_classes = self.model.detect_image(frame)
        return self.frame, self.box_count, self.predicted_classes


class YOLOPreprocess(Outputs):
    def __init__(self, outputs, duration):
        """
        Outputs format: [predicted_class, box_count]
        :param outputs: The format as up there
        :param duration: The duration of the video right now
        """
        super(YOLOPreprocess, self).__init__(outputs)

        self.duration = duration
        self.predicted_classes = outputs[0]

        self.all_classes = {}
        self.exist_classes = [x for x in self.predicted_classes]
        self.boxes = {}
        self.box_count = outputs[1]

    def process_outputs(self):
        set_classes = set(self.exist_classes)

        if self.duration not in self.boxes:
            self.boxes[self.duration] = {"box_count": 0, "classes": {}}

        self.boxes[self.duration]['box_count'] += self.box_count

        for _class in set_classes:
            self.all_classes.update({_class: self.exist_classes.count(_class)})

        self.boxes[self.duration]['classes'].update(self.all_classes)
        return self.boxes


class YOLOPreprocessWithAction(Outputs):
    def __init__(self, outputs, duration, tags_path):
        """
        Different from YOLOPreprocess, this class will also
        preprocess the outputs from the model. But also execute
        specific actions from the tags

        Outputs format: [predicted_class, box_count]
        :param outputs: The format as up there
        :param duration: The duration of the video right now
        """
        super(YOLOPreprocessWithAction, self).__init__(outputs)

        # Settings
        self.duration = duration

        self.predicted_classes = outputs[0]
        self.box_count = outputs[1]
        self.all_classes = {}
        self.exist_classes = [x for x in self.predicted_classes]
        self.boxes = {}
        self.tags_path = tags_path

        # The tags which we defined
        self.labelsWithTagObjs = Factory(
            basePaths(self.tags_path).joinBase()
        ).process()

    def process_outputs(self) -> dict:
        set_classes = set(self.exist_classes)

        if self.duration not in self.boxes:
            self.boxes[self.duration] = {"box_count": 0, "classes": {}, 'tags': []}

        self.boxes[self.duration]['box_count'] += self.box_count

        for _class in set_classes:
            self.boxes[self.duration]['tags'].append(self.labelsWithTagObjs[_class])

            self.all_classes.update({_class: self.exist_classes.count(_class)})

        self.boxes[self.duration]['classes'].update(self.all_classes)

        for ObjTags in self.boxes[self.duration]['tags']:
            for ObjTag in ObjTags:
                ObjTag().action()

        return self.boxes


class YOLOPreprocessWithTarget(Outputs):
    def __init__(self, outputs, duration, target):
        """
        This class are also same at processing outputs but
        with more advanced feature which calculate the times
        which class exist set by the user

        Outputs format: [predicted classes, box_count]
        :param outputs: The format as up there
        :param duration: The duration of the video right now
        :param target: The target we want to find
        """
        super(YOLOPreprocessWithTarget, self).__init__(outputs)

        self.target = target
        self.duration = duration
        self.predicted_classes = outputs[0]

        self.all_classes = {}
        self.exist_classes = [x for x in self.predicted_classes]
        self.boxes = {}
        self.box_count = outputs[1]

        self.targetTotal = 0

    def process_outputs(self) -> (dict, int):
        """
        :return: boxes dict and your target total exist times
        """

        set_classes = set(self.exist_classes)

        if self.duration not in self.boxes:
            self.boxes[self.duration] = {"box_count": 0, "classes": {}}

        self.boxes[self.duration]['box_count'] += self.box_count

        for _class in set_classes:
            count = self.exist_classes.count(_class)
            if _class is self.target:
                self.targetTotal += count

            self.all_classes.update({_class: count})

        self.boxes[self.duration]['classes'].update(self.all_classes)
        return self.boxes, self.targetTotal
