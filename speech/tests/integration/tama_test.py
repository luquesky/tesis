#! coding:utf-8
import math
import csv
import os
from unittest import TestCase
from ... import Speech, tama, WordInterval, FeatureExtractor, SpeechBuilder

DATA_DIR = os.getcwd() + "/speech/tests/integration/data"

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        speech = SpeechBuilder("speech/tests/integration/data/test.wav").speech
        tama(speech, "F0_MEAN", frame_step=2, frame_length=4)


    # The wav we use here has 20.87 seconds =>
    # Using frame_step = 2, and frame_length = 4 => there should be 10 frames! (the last one should be chopped)

    def test_tama_returns_the_right_number_of_frames(self):
        speech = SpeechBuilder("speech/tests/integration/data/test.wav").speech
        T, moving_average = tama(speech, "F0_MEAN", frame_step=2, frame_length=4)

        self.assertEqual(len(moving_average), 10)

    def test_tama_return_not_nan_values(self):
        speech = SpeechBuilder("speech/tests/integration/data/test.wav").speech

        T, moving_average = tama(speech, "F0_MEAN", frame_step=2, frame_length=4)

        self.assertTrue(all(not math.isnan(x) for x in moving_average ))
