#! coding:utf-8
from unittest import TestCase
from sympy import Interval
from ... import WordInterval
from .. import PhonemeExtractor

class PhonemeExtractorTest(TestCase):
    def test_it_contains_the_number_of_PHONEMES_and_its_average(self):
        extractor = PhonemeExtractor([WordInterval(0, 1, "hello")], {"hello" : 2})

        features = extractor.extract_features(Interval(0,1))

        self.assertIn("PHONEMES_COUNT", features.keys())
        self.assertIn("PHONEMES_AVG", features.keys())

    def test_it_returns_the_correct_count(self):
        extractor = PhonemeExtractor([
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], {
                "hello": 2,
                "how": 1
            })

        features = extractor.extract_features(Interval(0,1))

        self.assertEqual(features["PHONEMES_COUNT"], 3)

    def test_it_returns_the_correct_average(self):
        extractor = PhonemeExtractor([
            WordInterval(0, 0.5, "hello"),
            WordInterval(0.5, 1, "how")
            ], {
                "hello": 2,
                "how": 1
        })

        features = extractor.extract_features(Interval(0,0.5))

        self.assertAlmostEqual(features["PHONEMES_AVG"], 2 / 0.5)

    def test_it_looks_for_words_without_punctuation(self):
        extractor = PhonemeExtractor([
            WordInterval(0, 0.5, "he--llo?"),
            ], {
                "hello": 2,
                "how": 1
        })

        features = extractor.extract_features(Interval(0,0.5))

        self.assertAlmostEqual(features["PHONEMES_COUNT"], 2)
