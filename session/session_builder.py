#! coding:utf-8
import os
import csv
from . import Session
from task import Task
from speech import SpeechMapper

class SessionBuilder(object):
    def __init__(self, path_to_tasks):
        self.path_to_tasks = os.path.abspath(path_to_tasks)

    @property
    def session(self):
        speechA, speechB = self.__build_speechs()
        tasks = self.__build_tasks()

        return Session(tasks, speechA, speechB)

    def __build_speechs(self):
        filename, extension = os.path.splitext(self.path_to_tasks)

        path_to_A = "%s.A.wav" % filename
        path_to_B = "%s.B.wav" % filename

        # This is somehow nasty... but well...
        mapper = SpeechMapper()

        return mapper.fetch(path_to_A), mapper.fetch(path_to_B)

    def __build_tasks(self):
        tasks = []
        with open(self.path_to_tasks) as tasks_file:
            rows = csv.reader(tasks_file, delimiter=" ")
            for row in rows:
                begin = float(row[0])
                end = float(row[1])
                description = row[2]

                if (description != "#") and (description != "comments"):
                    task = Task(begin, end, description)
                    tasks.append(task)
        return tasks