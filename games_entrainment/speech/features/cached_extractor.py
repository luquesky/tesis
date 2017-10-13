#! coding:utf-8
import logging

logger = logging.getLogger('main')

class CachedExtractor(object):
    def __init__(self, extractor):
        self.extractor = extractor
        self.cached_features = {}

    def extract_features(self, interval):
        if not self.cached_features.has_key(interval):
            features = self.extractor.extract_features(interval)
            self.cached_features[interval] = features

        return self.cached_features[interval]
