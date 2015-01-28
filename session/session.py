#! coding:utf-8
import logging
import math
import numpy as np
from operator import itemgetter
from tama import hybrid_tama
from helpers import cross_correlation

logger = logging.getLogger('main')

class Session(object):
    def __init__(self, path_to_tasks, tasks, speechA, speechB):
        self.tasks = tasks
        self.path_to_tasks = path_to_tasks
        self.speechA = speechA
        self.speechB = speechB
        self.tamas = {}

    # Analyze with tama each task of the session
    def analyze(self, features=[]):
        if len(self.tamas) == 0:
            for task in self.tasks:
                logger.info("Working in task: %s" % task)
                self.tamas[task] = self.analyze_task(task, features=features)

        return self.tamas

    def analyze_task(self, task, features):
        ret = {}
        for feature in features:
            ret[feature] = self.analyze_task_feature(task, feature=feature)
        return ret

    def analyze_task_feature(self, task, feature):
        print "Calculating %s" % feature

        TA, averagesA = hybrid_tama(self.speechA, feature, interpolate=False, interval=task.interval)
        TB, averagesB = hybrid_tama(self.speechB, feature, interpolate=False, interval=task.interval)


        assert np.array_equal(TA, TB)
        n = len(TA)

        lags = range(-n, n+1)
        cross_correlations = [(lag, cross_correlation(averagesA, averagesB, lag)) for lag in lags]

        # lag > 0
        positive_correlations = [(l, cc) for (l, cc) in cross_correlations if l > 0]
        negative_correlations = [(l, cc) for (l, cc) in cross_correlations if l < 0]

        l_pos, cc_pos = max(positive_correlations, key=itemgetter(1))
        l_neg, cc_neg = max(negative_correlations, key=itemgetter(1))

        confidence_value = 2 / math.sqrt(n)

        return {
            "A": (TA, averagesA),
            "B": (TB, averagesB),
            "cross_correlations": cross_correlations,
            "confidence_value": confidence_value,
            "best_positive_lag": (l_pos, cc_pos),
            "best_negative_lag": (l_neg, cc_neg)
        }


