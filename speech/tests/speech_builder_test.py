#! coding:utf-8
import math
import csv
import os
from unittest import TestCase
from .. import Speech, SpeechBuilder, WordInterval

class SpeechBuilderTest(TestCase):
    def test_it_builds_it_with_correct_word_intervals(self):
        builder = SpeechBuilder("tama/tests/data/test.words")
        speech = builder.speech
        self.assertEqual(len(speech.utterances), 2)
