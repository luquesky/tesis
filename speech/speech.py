#! coding:utf-8
from helpers import build_utterances

class Speech(object):
    def __init__(self, path_to_wav, word_intervals, feature_extractor=None):
        self.path_to_wav = path_to_wav
        self.length = word_intervals[-1].sup
        self.utterances = build_utterances(word_intervals)
        self.feature_extractor = feature_extractor

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)

