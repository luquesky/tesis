#! coding:utf-8
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