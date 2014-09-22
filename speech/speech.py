#! coding:utf-8
from sympy import Interval
from helpers import build_utterances

class Speech(object):
    def __init__(self, word_intervals, feature_extractor=None):
        self.word_intervals = word_intervals
        self.utterances = build_utterances(word_intervals)
        self.feature_extractor = feature_extractor

    def length(self):
        return self.word_intervals[-1].sup

    def intervals_overlapping(self, frame):
        intervals = []
        for utterance in self.utterances:
            intersection = utterance.intersect(frame)
            # Not an empty set' nor a singleton
            if intersection.measure > 0:
                intervals.append(intersection)
        return intervals

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)




