#! coding:utf-8
from unittest import TestCase
from .. import WordInterval

class WordIntervalTest(TestCase):
    def test_inf_and_sup_are_correctly_set(self):
        interval = WordInterval(0, 14, "#")

        self.assertEqual(interval.inf, 0)
        self.assertEqual(interval.sup, 14)

    def test_equality_returns_true_for_equal_speech_intervals(self):
        self.assertEqual(WordInterval(0, 14, '#'), WordInterval(0, 14, '#'))

    def test_equality_returns_false_for_intervals_not_matching_words(self):
        self.assertNotEqual(WordInterval(0, 14, 'hi'), WordInterval(0, 14, 'bye'))

    def test_equality_returns_false_for_intervals_not_matching_limits(self):
        self.assertNotEqual(WordInterval(0, 14, 'hi'), WordInterval(1, 14, 'hi'))
