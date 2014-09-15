#! coding:utf-8
class Speech(object):
    def __init__(self, speech_intervals):
        self.speech_intervals = speech_intervals

    def length(self):
        return self.speech_intervals[-1].sup

    def intervals_overlapping(self, frame):
        intervals = []
        for interval in self.speech_intervals:
            intersection = interval.intersect(frame)
            if not intersection.is_EmptySet:
                intervals.append(intersection)
        return intervals