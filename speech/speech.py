#! coding:utf-8
from sympy import Interval

SPEECH_INTERVAL_THRESHOLD = 0.5

class Speech(object):
    def __init__(self, word_intervals, feature_extractor=None):
        self.word_intervals = word_intervals
        self.utterances = build_utterances(word_intervals)
        self.feature_extractor = feature_extractor

    def length(self):
        return self.word_intervals[-1].sup

    def intervals_overlapping(self, frame):
        intervals = []
        for interval in self.utterances:
            intersection = interval.intersect(frame)
            # Not an empty set' nor a singleton
            if intersection.measure > SPEECH_INTERVAL_THRESHOLD:
                intervals.append(intersection)
        return intervals

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)



def build_utterances(word_intervals):
    current_interval = None
    is_current_interval_silent = None
    speech_intervals = []

    for word_interval in word_intervals:
        if not current_interval:
            current_interval = Interval(word_interval.inf, word_interval.sup)
            is_current_interval_silent = word_interval.is_silent
        else:
            # If they are both silent, or both nonsilent => merge
            if bool(word_interval.is_silent) == bool(is_current_interval_silent):
                current_interval = Interval(current_interval.inf, word_interval.sup)
            # If not, push current
            else:
                speech_intervals.append(current_interval)
                current_interval = Interval(word_interval.inf, word_interval.sup)
                is_current_interval_silent = word_interval.is_silent

    if current_interval:
        speech_intervals.append(current_interval)

    return speech_intervals
