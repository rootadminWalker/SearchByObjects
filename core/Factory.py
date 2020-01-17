#!/usr/bin/evn python3
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

import json
from core.COCO_classes_tag import *

class Factory:
    def __init__(self, json_path):
        """
        A OOP factory architecture class to process
        the labels

        json_format:
            class: [tag1, tag2, tag3]

        :param json_path: The json you want to process
        """

        self.annotations = json.load(open(json_path, "r"))

        self.tags = {
            "Animal": Animal,
            "DailyItem": DailyItem,
            "Furniture": Furniture,
            "Tableware": Tableware,
            "SportsItem": SportsItem,
            "Food": Food,
            "ElectricalDevice": ElectricalDevice,
            "Transport": Transport
        }

        self.all_tags = {}
        self.all_objects = []

    def process(self) -> dict:
        """
        Process the tags

        :return: A dict with class as keys and tagObjects as value
        """
        for classes, values in self.annotations.items():
            tmp = []
            for tag in values:
                tmp.append(self.tags[tag])

            self.all_tags[classes] = tmp

        return self.all_tags


if __name__ == '__main__':
    json_path = '../models/COCO_classes_with_tag.json'
    f = Factory(json_path)
    f.process()
    print(f.all_tags)
