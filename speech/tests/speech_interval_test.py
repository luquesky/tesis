#! coding:utf-8
from unittest import TestCase
from .. import SpeechInterval

class SpeechIntervalTest(TestCase):
    def test_inf_and_sup_are_correctly_set(self):
        interval = SpeechInterval(0, 14, "#")

        self.assertEqual(interval.inf, 0)
        self.assertEqual(interval.sup, 14)

    def test_equality_returns_true_for_equal_speech_intervals(self):
        self.assertEqual(SpeechInterval(0, 14, '#'), SpeechInterval(0, 14, '#'))

    def test_equality_returns_false_for_intervals_not_matching_words(self):
        self.assertNotEqual(SpeechInterval(0, 14, 'hi'), SpeechInterval(0, 14, 'bye'))

    def test_equality_returns_false_for_intervals_not_matching_limits(self):
        self.assertNotEqual(SpeechInterval(0, 14, 'hi'), SpeechInterval(1, 14, 'hi'))
