#! coding:utf-8
class Speech(object):
    def __init__(self, speech_intervals, feature_extractor=None):
        self.speech_intervals = speech_intervals
        self.feature_extractor = feature_extractor

    def length(self):
        return self.speech_intervals[-1].sup

    def intervals_overlapping(self, frame):
        intervals = []
        for interval in self.speech_intervals:
            intersection = interval.intersect(frame)
            if not intersection.is_EmptySet:
                intervals.append(intersection)
        return intervals

    def get_features(self, interval):
        self.feature_extractor.extract_features(interval)