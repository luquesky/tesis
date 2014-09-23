#! coding:utf-8
import math
import csv
import os
from unittest import TestCase
from .. import Speech, SpeechBuilder, WordInterval

class SpeechBuilderTest(TestCase):
    def test_it_builds_it_with_correct_word_intervals(self):
        builder = SpeechBuilder("speech/tests/integration/data/test.words")
        speech = builder.speech
        self.assertEqual(len(speech.utterances), 2)

    def test_it_builds_with_feature_extractor(self):
        path_to_wav = "speech/tests/integration/data/test.words"
        builder = SpeechBuilder(path_to_wav)
        speech = builder.speech
        self.assertEqual(speech.feature_extractor.path_to_wav, os.path.abspath(path_to_wav))
