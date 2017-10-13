#! coding:utf-8
# This extractor combines several extractors into one
import logging

logger = logging.getLogger('main')

class CompositeExtractor(object):

    # All paths should be absolute...praat
    def __init__(self, *extractors):
        self.extractors = extractors

    def extract_features(self, interval):
        features = {}

        for extractor in self.extractors:
            new_features = extractor.extract_features(interval)
            features.update(new_features)

        return features
