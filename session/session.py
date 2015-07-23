#! coding:utf-8
import logging
import math
import numpy as np
from operator import itemgetter

logger = logging.getLogger('main')


class Session(object):
    def __init__(self, path_to_tasks, name, number, tasks):
        self.tasks = tasks
        self.path_to_tasks = path_to_tasks
        self.name = name
        self.number = number
        self.tamas = {}
