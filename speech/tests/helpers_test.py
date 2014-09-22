#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import Speech, WordInterval
from ..helpers import build_utterances, intervals_overlapping

class BuildUtterancesTest(TestCase):
    def test_it_merges_silence(self):
        word_intervals = [WordInterval(0, 14, WordInterval.SILENCE_WORD), WordInterval(14, 18, WordInterval.SILENCE_WORD)]
        self.assertEqual(build_utterances(word_intervals), [Interval(0, 18)] )

    def test_it_merges_non_silence(self):
        word_intervals = [
            WordInterval(0, 14, 'high'),
            WordInterval(14, 18, 'five')]
        self.assertEqual(build_utterances(word_intervals), [Interval(0, 18)] )

    def test_it_merges_both(self):
        word_intervals = [
            WordInterval(0, 14, 'high'),
            WordInterval(14, 18, 'five'),
            WordInterval(18, 20, WordInterval.SILENCE_WORD),
            WordInterval(20, 22, 'huh?'),
        ]
        self.assertEqual(build_utterances(word_intervals),
            [Interval(0, 18), Interval(18, 20), Interval(20, 22)] )

class IntervalsOverlappingTest(TestCase):
    def test_intervals_overlapping_for_included_interval(self):
        speech = Speech(word_intervals=[
            WordInterval(0, 14, "#"),
        ])

        self.assertEqual(intervals_overlapping(speech, Interval(0, 14)), [Interval(0, 14)])

    def test_intervals_overlapping_for_merged_non_silent_intervals(self):
        speech = Speech(word_intervals=[
            WordInterval(0, 14.0, "#"),
            WordInterval(14.0, 14.5, "hi"),
            WordInterval(14.5, 15.5, "frank")
        ])

        interval = Interval(14, 15.5)

        self.assertItemsEqual(intervals_overlapping(speech, Interval(13.0, 16.0)), [Interval(13.0, 14.0), Interval(14.0, 15.5)])