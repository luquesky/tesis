#! coding:utf-8
import bisect

class SyllabeExtractor(object):
    def __init__(self, word_intervals, syllabes_count):
        self.word_intervals = word_intervals
        self.syllabes_count = syllabes_count
        self.supremes = [wint.sup for wint in self.word_intervals]

    def extract_features(self, interval):
        count = self.count_syllabes(interval)

        return {
            "SYLLABES_COUNT": count,
            "SYLLABES_AVG": float(count) / interval.measure
        }

    def count_syllabes(self, interval):
        count = 0
        index = bisect.bisect_left(self.supremes, interval.inf)

        if index == len(self.word_intervals):
            return 0

        while index < len(self.word_intervals):
            word_interval = self.word_intervals[index]

            intersection = word_interval.intersect(interval.closure)

            if intersection.measure > 0:
                count += self.syllabes_count[word_interval.word]
            elif intersection.is_EmptySet:
                break
            index+=1

        return count
