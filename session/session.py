#! coding:utf-8
import logging
from tama import hybrid_tama

logger = logging.getLogger('main')

class Session(object):
    def __init__(self, path_to_tasks, tasks, speechA, speechB):
        self.tasks = tasks
        self.path_to_tasks = path_to_tasks
        self.speechA = speechA
        self.speechB = speechB

    # Analyze with tama each task of the session
    def analyze(self, features=[]):
        tamas = {}
        for task in self.tasks:
            tamas[task] = {}
            print "Working in task: %s" % task
            for feature in features:
                tamas[task][feature] = {}
                print "Calculating %s" % feature
                tamas[task][feature]["A"] = hybrid_tama(self.speechA, feature, interpolate=False, interval=task.interval)
                tamas[task][feature]["B"] = hybrid_tama(self.speechB, feature, interpolate=False, interval=task.interval)
        return tamas