#! coding:utf-8
"""Session Builder class."""
import os
import csv
import re
from sympy import Interval
from . import Session
from task import Task
from ..speech import SpeechBuilder


class SessionBuilder(object):
    """Builder of sessions.

    Given the parameters of the session (number, path to tasks, and others)
    it builds the Session object with its tasks and so on

    Parameters
    ----------

    path_to_tasks :
        Path to task directory
    session_info: dataframe
        Information of each session: id and gender of speakers
    number : integer
        Number of the session (between 1 and 12)
    options : dict
        Optional arguments, such as name
    """

    def __init__(self, path_to_tasks, number, idA, genderA, idB, genderB, **options):
        """Constructor."""
        self.name = options.get('name') or path_to_tasks
        self.number = int(number)
        self.idA = idA
        self.idB = idB
        self.genderA = genderA
        self.genderB = genderB
        self.path_to_tasks = os.path.abspath(path_to_tasks)

    @property
    def session(self):
        """Return the built session."""
        tasks = self.__build_tasks()

        return Session(
            tasks=tasks,
            path_to_tasks=self.path_to_tasks,
            name=self.name,
            number=self.number
        )

    def __build_tasks(self):
        tasks = []
        with open(self.path_to_tasks) as tasks_file:
            rows = csv.reader(tasks_file, delimiter=" ")
            index = 0
            for row in rows:

                begin = float(row[0])
                end = float(row[1])
                interval = Interval(begin, end)
                description = row[2]

                if re.match(r'Images.*', description):
                    index += 1
                    task = self.__build_task(
                        index, description=description, interval=interval)
                    tasks.append(task)
        return tasks

    def __build_task(self, task_number, description, interval):
        name = "Task-%s" % str(task_number).zfill(2)
        speechA, speechB = self.__build_speechs(interval)
        return Task(interval,
                    number=task_number,
                    speechA=speechA,
                    speechB=speechB,
                    description=description,
                    name=name)

    def __build_speechs(self, interval):
        filename, extension = os.path.splitext(self.path_to_tasks)

        path_to_A = "%s.A.wav" % filename
        path_to_B = "%s.B.wav" % filename

        speechA = SpeechBuilder(path_to_A, interval, self.idA, self.genderA).speech
        speechB = SpeechBuilder(path_to_B, interval, self.idB, self.genderB).speech

        return speechA, speechB
