#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import SpeechBuilder

class SpeechBuilderTest(TestCase):
    def test_it_builds_it_with_correct_word_intervals(self):
        builder = SpeechBuilder("tama/tests/data/test.words",
            interval=Interval(0, 20.87),
            gender='m',
            speaker_id=101
        )

        speech = builder.speech
        self.assertEqual(len(speech.utterances), 2)

    def test_it_builds_with_utterances_contained_in_interval(self):
        builder = SpeechBuilder("tama/tests/data/test.words",
            interval=Interval(0, 15.0),
            gender='m',
            speaker_id=101
        )

        speech = builder.speech

        self.assertEqual(len(speech.utterances), 1)

