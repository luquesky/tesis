#! coding:utf-8
import bisect
import logging

logger = logging.getLogger('main')
# Sums the mapping of words contained in the interval
# Mapping should be a dict with domain of the words, and with numeric values
# Common examples: count the syllabes, and phonemes
class WordMappingExtractor(object):
    def __init__(self, word_intervals, mapping, feature_name):
        self.word_intervals = word_intervals
        self.mapping = mapping
        self.supremes = [wint.sup for wint in self.word_intervals]
        self.feature_name = feature_name

    def extract_features(self, interval):
        count = self.sum_words_on_interval(interval)

        count_key = "%s_COUNT" % self.feature_name
        avg_key = "%s_AVG" % self.feature_name

        return {
            count_key: count,
            avg_key: float(count) / interval.measure
        }

    def sum_words_on_interval(self, interval):
        count = 0
        index = bisect.bisect_left(self.supremes, interval.inf)

        if index == len(self.word_intervals):
            return 0

        while index < len(self.word_intervals):
            word_interval = self.word_intervals[index]

            intersection = word_interval.intersect(interval.closure)

            if intersection.measure > 0:
                count += self.mapping(word_interval.word.lower())
            elif intersection.is_EmptySet:
                break
            index+=1

        return count

def SyllabeExtractor(word_intervals, syllabe_count):
    mapping = lambda word: syllabe_count[word]
    return WordMappingExtractor(word_intervals, mapping, feature_name="SYLLABES")

def PhonemeExtractor(word_intervals, phoneme_count):
    def mapping(word):
        try:
            preprocessed_word = "".join(w for w in word if w.isalpha() or w == '\'')
            return phoneme_count[preprocessed_word]
        except KeyError:
            logger.warning("%s(%s) has no defined phonemes. Defaulting to 0" % (word, preprocessed_word))
            return 0
    return WordMappingExtractor(word_intervals, mapping, feature_name="PHONEMES")