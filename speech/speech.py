#! coding:utf-8
from helpers import build_utterances

class Speech(object):
    def __init__(self, path_to_wav, word_intervals, feature_extractor=None):
        self.path_to_wav = path_to_wav
        self.word_intervals = word_intervals
        self.utterances = build_utterances(word_intervals)
        self.feature_extractor = feature_extractor

    @property
    def length(self):
        return self.word_intervals[-1].sup

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)

    @property
    def silent_intervals(self):
        return [interval for interval in self.word_intervals if interval.is_silent]
