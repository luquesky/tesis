#! coding:utf-8
import numpy as np
from mock import MagicMock
from sympy import Interval
from unittest import TestCase
from .. import Speech, WordInterval

class SpeechTest(TestCase):

    def test_length_returns_length_of_the_speech(self):
        speech = Speech(path_to_wav="", interval=Interval(0, 15),word_intervals=[
            WordInterval(0, 14, "#"),
            WordInterval(14, 14.5, "hi")
        ])

        self.assertAlmostEqual(speech.length, 15.0)

    def test_getting_features_for_an_interval_should_ask_feature_extractor_for_it(self):
        mock_extractor = MagicMock(spec=["extract_features"])

        speech = Speech(path_to_wav="", interval=Interval(0, 15), word_intervals=[
            WordInterval(0, 14, "#"),
            WordInterval(14, 14.5, "hi"),
            WordInterval(14.5, 15.5, "frank")
        ], feature_extractor= mock_extractor)
        interval = Interval(14, 14.5)

        speech.get_features(interval)

        mock_extractor.extract_features.assert_called_with(interval)

    def test_get_feature_for_a_not_existent_variable_returns_nan(self):
        extractor = MagicMock()
        extractor.extract_features.return_value = {}

        speech = Speech(path_to_wav="", interval=Interval(0, 15), feature_extractor=extractor, word_intervals=[])

        feature = speech.get_feature("F0_MEAN", interval=(0, 15))
        self.assertTrue(np.isnan(feature))


    def test_get_feature_for_a_nan_variable_returns_nan(self):
        extractor = MagicMock()
        extractor.extract_features.return_value = {"F0_MEAN": np.nan}

        speech = Speech(path_to_wav="", interval=Interval(0, 15), feature_extractor=extractor, word_intervals=[])

        feature = speech.get_feature("F0_MEAN", interval=(0, 15))
        self.assertTrue(np.isnan(feature))

    def test_get_feature_for_a_valid_value_returns_it(self):
        extractor = MagicMock()
        extractor.extract_features.return_value = {"F0_MEAN": 1.0}

        speech = Speech(path_to_wav="", interval=Interval(0, 15), feature_extractor=extractor, word_intervals=[])

        feature = speech.get_feature("F0_MEAN", interval=(0, 15))

        self.assertAlmostEqual(feature, 1.0)


    def test_it_sets_its_interval(self):
        interval = Interval(0, 15)
        speech = Speech(path_to_wav="", interval=interval,word_intervals=[])

        self.assertEqual(speech.interval, interval)




    def test_is_speaking_returns_false_when_silent_interval(self):
        mock_extractor = MagicMock(spec=["extract_features"])
        speech = Speech(path_to_wav="",
            interval=Interval(0, 15),
            word_intervals=[
                WordInterval(0, 14, "#"),
                WordInterval(14, 14.5, "hi"),
                WordInterval(14.5, 15.5, "frank")],
            feature_extractor= mock_extractor)

        self.assertFalse(speech.is_speaking_at(10.0))

    def test_is_speaking_returns_true_when_not_silent_interval(self):
        mock_extractor = MagicMock(spec=["extract_features"])
        speech = Speech(path_to_wav="",
            interval=Interval(0, 15),
            word_intervals=[
                WordInterval(0, 14, "#"),
                WordInterval(14, 14.5, "hi"),
                WordInterval(14.5, 15.5, "frank")],
            feature_extractor= mock_extractor)

        self.assertTrue(speech.is_speaking_at(14.25))
