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

from .base_classes import tag

"""
    This are tags for different model labels
"""

class Animal(tag):
    def __init__(self):
        super(Animal, self).__init__('animal')

    def action(self):
        print("We need to protect animals!")


class Transport(tag):
    def __init__(self):
        super(Transport, self).__init__('transport')

    def action(self):
        print("Let's go on a trip")


class DailyItem(tag):
    def __init__(self):
        super(DailyItem, self).__init__('daily item')

    def action(self):
        print("We see this every day")


class SportsItem(tag):
    def __init__(self):
        super(SportsItem, self).__init__('sports item')

    def action(self):
        print("Let's play sports")


class Tableware(tag):
    def __init__(self):
        super(Tableware, self).__init__('tableware')

    def action(self):
        print("Let's have dinner")


class Food(tag):
    def __init__(self):
        super(Food, self).__init__('food')

    def action(self):
        print("A lot of food")


class Furniture(tag):
    def __init__(self):
        super(Furniture, self).__init__('furniture')

    def action(self):
        print("Home")


class ElectricalDevice(tag):
    def __init__(self):
        super(ElectricalDevice, self).__init__('electrical device')

    def action(self):
        print("Electric")
