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

from .base_classes import Labels, Data
from .Factory import Factory
from .basePaths import basePaths
from flask import jsonify

"""
    Data processing class for website post operation
"""

class tagProcess(Labels):
    def __init__(self, json_path: str):
        """
        Process the tags json file by
        using different processor

        :param json_path: The path to your tags file. See Factory.py for more details
        """

        super(tagProcess, self).__init__(Factory)

        self.json_path = basePaths(json_path).joinBase()
        self.processed = {}

    def process(self) -> dict:
        """
        A processing with our Factory class

        :return: Processed dict
        """

        self.processed = self.processor(self.json_path).process()
        return self.processed


class jsonifyTagData(Data):
    def __init__(self, data: dict):
        """
        Inherited by the Data class. This will
        Jsonify your tag data

        :param data: The processed dict by tagProcess class
        """

        super(jsonifyTagData, self).__init__(data)
        self.result = []
        self.classes = {'classes': []}

    def action(self):
        """
        Jsonify it
        :return: The jsonify data
        """

        [self.result.append(item) for item in self.data.keys()]

        self.classes.update({'classes': self.result})
        return jsonify(self.classes)
