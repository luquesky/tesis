#! coding:utf-8

class SyllabeExtractor(object):
    def __init__(self, word_intervals, syllabes_count):
        self.word_intervals = word_intervals
        self.syllabes_count = syllabes_count

    def extract_features(self, interval):
        count = self.count_syllabes(interval)

        return {
            "SYLLABES_COUNT": count,
            "SYLLABES_AVG": float(count) / interval.measure
        }

    def count_syllabes(self, interval):
        count = 0

        for word_interval in self.word_intervals:
            if not word_interval.intersect(interval.interior).is_EmptySet:
                count += self.syllabes_count[word_interval.word]

        return count
