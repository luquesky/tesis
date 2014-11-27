#! coding:utf-8
from unittest import TestCase
from sympy import Interval
from ... import WordInterval
from .. import WordMappingExtractor

class WordMappingExtractorTest(TestCase):
    def test_it_contains_the_number_of_syllabes_and_its_average(self):
        extractor = WordMappingExtractor(word_intervals=[
            WordInterval(0, 1, "hello")
            ],
            mapping = {
                "hello" : 2
            },
            feature_name="SYLLABES"
        )

        features = extractor.extract_features(Interval(0,1))

        self.assertIn("SYLLABES_COUNT", features.keys())
        self.assertIn("SYLLABES_AVG", features.keys())

    def test_it_returns_the_correct_count(self):
        extractor = WordMappingExtractor(word_intervals=[
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], mapping ={
                "hello": 2,
                "how": 1
            }, feature_name ="SYLLABES")

        features = extractor.extract_features(Interval(0,1))

        self.assertEqual(features["SYLLABES_COUNT"], 3)

    def test_it_returns_the_correct_average(self):
        extractor = WordMappingExtractor(word_intervals=[
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], mapping ={
                "hello": 2,
                "how": 1
            }, feature_name="SYLLABES")

        features = extractor.extract_features(Interval(0,0.5))

        self.assertAlmostEqual(features["SYLLABES_AVG"], 2 / 0.5)


