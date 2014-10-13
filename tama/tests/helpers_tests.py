#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from speech import Speech, WordInterval
from ..helpers import intersecting_utterances, hybrid_intersecting_utterances, interpolate

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

class InterpolateTest(TestCase):
    def test_it_handles_zero_surrounded_by_non_zero(self):
        averages = [1.0, .0, 3.0]
        interpolate(averages)
        self.assertEqual(averages, [1.0, 2.0, 3.0])

    def test_it_handles_consecutive_zeros(self):
        averages = [1.0, .0, .0, 3.0]
        interpolate(averages)
        self.assertEqual(averages, [1.0, 1.0, 2.0, 3.0])

    def test_it_handles_leading_zeros(self):
        averages = [.0, .0, 3.0]
        interpolate(averages)
        self.assertEqual(averages, [.0, .0, 3.0])
