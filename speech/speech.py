#! coding:utf-8
import csv

class Speech(object):
    def __init__(self, intervals):
        self.intervals = intervals

    def length(self):
        length = 0
        for interval in self.intervals:
            length = interval[1]
        return length