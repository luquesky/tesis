#! coding:utf-8
# An object of this class has the responsibility of extracting the features (f_0, ) out of a wav file
# It should be created with both a path to the wav file, and to a praat script which returns the features (in the project, they are at scripts/)
import logging

logger = logging.getLogger('main')

class CompositeExtractor(object):

    # All paths should be absolute...praat
    def __init__(self, extractor1, extractor2):
        self.extractor1 = extractor1
        self.extractor2 = extractor2

    def extract_features(self, interval):
        features1 = self.extractor1.extract_features(interval)
        features2 = self.extractor2.extract_features(interval)

        features = features1.copy()
        features.update(features2)

        return features
