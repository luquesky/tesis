#! coding: utf-8
import os
import csv
from word_interval import WordInterval
from feature_extractor import FeatureExtractor
from speech import Speech

DATA_DIR = "speech/tests/integration/data"

class SpeechBuilder(object):
    def __init__(self, path_to_file):
        self.path_to_file = os.path.abspath(path_to_file)

    def get_word_intervals(self):
        intervals = []
        with open(self.path_to_file) as test_words:
            rows = csv.reader(test_words, delimiter=" ")
            for row in rows:
                intervals.append(WordInterval(float(row[0]), float(row[1]),row[2]))
        return intervals

    # This is quite ad hoc
    def build_feature_extractor(self):
        return FeatureExtractor(
            path_to_script = os.path.abspath("scripts/extractStandardAcoustics.praat"),
            path_to_praat = "/usr/local/bin/praat",
            path_to_wav=self.path_to_file
        )

    @property
    def speech(self):
        word_intervals = self.get_word_intervals()
        feature_extractor = self.build_feature_extractor()
        return Speech(word_intervals=word_intervals,
            feature_extractor=feature_extractor)