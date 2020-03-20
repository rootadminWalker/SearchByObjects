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

from abc import ABC, abstractmethod
import numpy as np

"""
    These methods are defined as base class for inherit
"""


# The detection base class for different models
class Detection(ABC):
    def __init__(self, model_path: str, classes_path: str):
        """
        Use different models to predict more
        confident by inherit this class to your
        class

        :param model_path: Path to your model
        :param classes_path: Path to your labels
        """

        self.model_path = model_path
        self.classes_path = classes_path

    @abstractmethod
    def detect(self, frame: np.array):
        """
        Use different methods to predict
        your image

        :param frame: The image your want to predict
        :return: Anything you set when you inherit this class
        """
        pass


# The output processing base class for different model outputs
class Outputs(ABC):
    def __init__(self, outputs):
        """
        A class for you to do process to your
        model outputs

        :param outputs: The outputs from the model
        """
        self.outputs = outputs

    @abstractmethod
    def process_outputs(self):
        """
        Process output

        :return: Your choice
        """
        pass


# The image processing base class for different model image preprocess
class Img(ABC):
    def __init__(self, img):
        """
        Preprocess your image before
        passing to the model

        :param img:
        """
        self.img = img

    @abstractmethod
    def preprocess_to(self):
        """
        Preprocess code

        :return: Your choice
        """
        pass

    @abstractmethod
    def rollback(self):
        """
        Process back to your original image
        (If you need it)

        :return: Your choice
        """
        pass


# The tag base class is used to process the labels
class tag(ABC):
    def __init__(self, name: str):
        """
        The categories of your labels

        :param name: The name of the tag
        """
        self.name = name

    @abstractmethod
    def action(self):
        """
        The program when you saw specific
        category

        :return: Your choice
        """
        pass


# Use a label processor to process the model labels
class Labels(ABC):
    def __init__(self, processor):
        """
        Process your labels before training
        or predict

        :param processor: The processor you want to process to the labels
        """
        self.processor = processor

    @abstractmethod
    def process(self):
        """
        Your processing code

        :return: Your choice
        """
        pass


# Process to output data from model when operating post operation on websites
class Data(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def action(self):
        pass
