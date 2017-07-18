#! coding:utf-8
"""Speech class."""
import numpy as np
from bisect import bisect_left
from helpers import build_utterances


class Speech(object):
    """Represent the speech of one of the participants at a session."""

    def __init__(self, path_to_wav, interval, word_intervals, gender, feature_extractor=None):
        """Constructor.

        Parameters:
        -----------

        path_to_wav: string
            path to wav file.
        interval: sympy.Interval
            Interval in seconds of the given wav.
        word_intervals: list of WordInterval
            Intervals of words
        feature_extractor: FeatureExtractor
            Something to extract features from
        """
        self.path_to_wav = path_to_wav
        self.utterances = build_utterances(word_intervals)
        # TODO: Try to refactor this
        self.supremes = [utt.sup for utt in self.utterances]
        self.interval = interval
        self.gender = gender
        self.feature_extractor = feature_extractor

    @property
    def length(self):
        return self.interval.measure

    def get_features(self, interval):
        return self.feature_extractor.extract_features(interval)

    def get_feature(self, feature, interval):
        features = self.get_features(interval)

        if not features.has_key(feature):
            return np.nan
        else:
            return features[feature]

    def is_speaking_at(self, time):
        index = bisect_left(self.supremes, time)

        if index == len(self.supremes):
            return False

        utterance = self.utterances[index]

        return utterance.contains(time)