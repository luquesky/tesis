#! coding:utf-8
from unittest import TestCase
from sympy import Interval
from ... import WordInterval
from .. import WordMappingExtractor, SyllabeExtractor

class SyllabeExtractorTest(TestCase):
    def test_it_contains_the_number_of_syllabes_and_its_average(self):
        extractor = SyllabeExtractor([WordInterval(0, 1, "hello")], {"hello" : 2})

        features = extractor.extract_features(Interval(0,1))

        self.assertIn("SYLLABES_COUNT", features.keys())
        self.assertIn("SYLLABES_AVG", features.keys())

    def test_it_returns_the_correct_count(self):
        extractor = SyllabeExtractor([
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], {
                "hello": 2,
                "how": 1
            })

        features = extractor.extract_features(Interval(0,1))

        self.assertEqual(features["SYLLABES_COUNT"], 3)

    def test_it_returns_the_correct_average(self):
        extractor = SyllabeExtractor([
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], {
                "hello": 2,
                "how": 1
        })

        features = extractor.extract_features(Interval(0,0.5))

        self.assertAlmostEqual(features["SYLLABES_AVG"], 2 / 0.5)


