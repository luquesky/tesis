#! coding:utf-8
from bisect import bisect_left
from helpers import build_utterances

class Speech(object):
    def __init__(self, path_to_wav, interval, word_intervals, feature_extractor=None):
        self.path_to_wav = path_to_wav
        self.length = word_intervals[-1].sup
        self.utterances = build_utterances(word_intervals)
        # TODO: Try to refactor this
        self.supremes = [utt.sup for utt in self.utterances]

        self.feature_extractor = feature_extractor

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)

    def is_speaking_at(self, time):
        index = bisect_left(self.supremes, time)

        if index == len(self.supremes):
            return False

        utterance = self.utterances[index]

        return utterance.contains(time)