#! coding:utf-8
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
        self.assertEqual(speech.length, 14.5)

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
