#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import Speech, WordInterval
from ..helpers import build_utterances, intersecting_utterances, hybrid_intersecting_utterances

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

class IntervalsOverlappingTest(TestCase):
    def test_intervals_overlapping_for_included_interval(self):
        speech = Speech(word_intervals=[
            WordInterval(0, 14, "woooow"),
        ])

        self.assertEqual(intersecting_utterances(speech, Interval(0, 14)), [Interval(0, 14)])

    def test_intervals_overlapping_for_merged_non_silent_intervals(self):
        speech = Speech(word_intervals=[
            WordInterval(0, 14.0, WordInterval.SILENCE_WORD),
            WordInterval(14.0, 14.5, "hi"),
            WordInterval(14.5, 15.5, "frank")
        ])
        interval = Interval(13.0, 16.0)

        self.assertItemsEqual(intersecting_utterances(speech, interval), [Interval(14.0, 15.5)])

class HybridIntersectingUtterancesTest(TestCase):
    def test_intervals_overlapping_for_included_interval(self):
        speech = Speech(word_intervals=[
            WordInterval(0, 14, "#"),
        ])

        self.assertEqual(hybrid_intersecting_utterances(speech, Interval(0, 14)), [])

    def test_intervals_overlapping_for_merged_non_silent_intervals(self):
        speech = Speech(word_intervals=[
            WordInterval(0.0, 14.0, "#"),
            WordInterval(14.0, 14.5, "hi"),
            WordInterval(14.5, 15.5, "frank")
        ])

        self.assertItemsEqual(hybrid_intersecting_utterances(speech, Interval(13.0, 15.0)),
            [Interval(14.0, 15.5)])