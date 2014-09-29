#! coding:utf-8
from helpers import build_utterances

class Speech(object):
    def __init__(self, word_intervals, feature_extractor=None):
        self.word_intervals = word_intervals
        self.utterances = build_utterances(word_intervals)
        self.feature_extractor = feature_extractor

    def length(self):
        return self.word_intervals[-1].sup

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)
