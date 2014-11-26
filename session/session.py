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
            print "Working in task: %s" % task
            tamas[task] = self.analyze_task(task, features)
        return tamas

    def analyze_task(self, task, features=[]):
        ret = {}
        for feature in features:
            ret[feature] = {}
            print "Calculating %s" % feature
            ret[feature]["A"] = hybrid_tama(self.speechA, feature, interpolate=False, interval=task.interval)
            ret[feature]["B"] = hybrid_tama(self.speechB, feature, interpolate=False, interval=task.interval)
        return ret
