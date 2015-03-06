#! coding:utf-8
import os
import csv
import re
from sympy import Interval
from . import Session
from task import Task
from speech import SpeechBuilder

class SessionBuilder(object):
    def __init__(self, path_to_tasks):
        self.path_to_tasks = os.path.abspath(path_to_tasks)

    @property
    def session(self):
        #speechA, speechB = self.__build_speechs()
        tasks = self.__build_tasks()

        return Session(tasks=tasks, path_to_tasks=self.path_to_tasks)


    def __build_tasks(self):
        tasks = []
        with open(self.path_to_tasks) as tasks_file:
            rows = csv.reader(tasks_file, delimiter=" ")
            for row in rows:
                begin = float(row[0])
                end = float(row[1])
                interval = Interval(begin, end)
                description = row[2]

                speechA, speechB = self.__build_speechs(interval)

                if re.match(r'Images.*', description):
                    task = Task(interval, speechA=speechA, speechB=speechB, description=description)
                    tasks.append(task)
        return tasks

    def __build_speechs(self, interval):
        filename, extension = os.path.splitext(self.path_to_tasks)

        path_to_A = "%s.A.wav" % filename
        path_to_B = "%s.B.wav" % filename

        return SpeechBuilder(path_to_A, interval).speech, SpeechBuilder(path_to_B, interval).speech