#! coding:utf-8
import math
from unittest import TestCase
from mock import Mock
from sympy import Interval
from speech import SpeechBuilder
from tama import tama


class TamaTest(TestCase):
    # The wav we use here has 20.87 seconds =>
    # Using frame_step = 2, and frame_length = 4 => there should be 10 frames! (the last one should be chopped)

    def test_tama_returns_the_right_number_of_frames(self):
        speech = SpeechBuilder("tama/tests/data/test.wav", interval=Interval(0, 30)).speech

        series, mean = tama(speech, "F0_MEAN", frame_step=3, frame_length=4)

        self.assertEqual(len(series), 10)

    def test_tama_return_correct_t(self):
        speech = SpeechBuilder("tama/tests/data/test.wav", interval=Interval(0, 30)).speech

        series, mean = tama(speech, "F0_MEAN", frame_step=3, frame_length=4)

        self.assertTrue((series.index == [3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0]).all())

    def test_tama_works_for_a_specified_interval(self):
        speech = SpeechBuilder("tama/tests/data/test.wav", interval=Interval(0, 30)).speech

        series, mean = tama(speech, "F0_MEAN", frame_step=3, frame_length=4, interpolate=False, interval=Interval(13, 20))

        self.assertTrue((series.index == [16.0, 19.0]).all())

