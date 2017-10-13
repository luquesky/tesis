#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import WordInterval
from ..helpers import build_utterances

class BuildUtterancesTest(TestCase):
    def test_it_merges_silence(self):
        word_intervals = [WordInterval(0, 14, WordInterval.SILENCE_WORD), WordInterval(14, 18, WordInterval.SILENCE_WORD)]
        self.assertEqual(build_utterances(word_intervals), [] )

    def test_it_merges_non_silence(self):
        word_intervals = [
            WordInterval(0, 14, 'high'),
            WordInterval(14, 18, 'five')]
        self.assertEqual(build_utterances(word_intervals), [Interval(0, 18)] )

    def test_it_merges_both(self):
        word_intervals = [
            WordInterval(0, 4, WordInterval.SILENCE_WORD),
            WordInterval(4, 14, 'high'),
            WordInterval(14, 18, 'five'),
            WordInterval(18, 20, WordInterval.SILENCE_WORD),
            WordInterval(20, 22, 'huh?'),
            WordInterval(22, 28, WordInterval.SILENCE_WORD),
        ]
        self.assertEqual(build_utterances(word_intervals),
            [Interval(4, 18), Interval(20, 22)] )
