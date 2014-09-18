#! coding:utf-8
from mock import MagicMock
from sympy import Interval
from unittest import TestCase
from .. import Speech, SpeechInterval

class SpeechTest(TestCase):

    def setUp(self):
        pass

    def test_length_returns_length_of_the_speech(self):
        speech = Speech(speech_intervals=[
            SpeechInterval(0, 14, "#"),
            SpeechInterval(14, 14.5, "hi")
        ])
        self.assertEqual(speech.length(), 14.5)

    def test_intervals_overlapping_for_included_interval(self):
        speech = Speech(speech_intervals=[
            SpeechInterval(0, 14, "#"),
        ])

        self.assertEqual(speech.intervals_overlapping(Interval(0, 14)), [Interval(0, 14)])

    def test_getting_features_for_an_interval_should_ask_feature_extractor_for_it(self):
        mock_extractor = MagicMock(spec=["extract_features"])

        speech = Speech(speech_intervals=[
            SpeechInterval(0, 14, "#"),
            SpeechInterval(14, 14.5, "hi")
        ], feature_extractor= mock_extractor)
        interval = Interval(14, 14.5)

        speech.get_features(interval)

        mock_extractor.extract_features.assert_called_with(interval)
