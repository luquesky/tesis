#! coding:utf-8
import math
from sympy import Interval
from unittest import TestCase
from speech import SpeechBuilder
from tama import Calculator

class TamaTest(TestCase):
    # The wav we use here has 20.87 seconds =>
    # Using frame_step = 2, and frame_length = 4 => there should be 10 frames! (the last one should be chopped)

    def test_tama_returns_the_right_number_of_frames(self):
        speech = SpeechBuilder("tama/tests/data/test.wav").speech

        calculator = Calculator(speech, frame_step=2, frame_length=4)

        T, moving_average = calculator.calculate("F0_MEAN")

        self.assertEqual(len(moving_average), 10)

    def test_tama_return_not_nan_values(self):
        speech = SpeechBuilder("tama/tests/data/test.wav").speech

        calculator = Calculator(speech, frame_step=2, frame_length=4)

        T, moving_average = calculator.calculate("F0_MEAN")


        self.assertTrue(all(not math.isnan(x) for x in moving_average ))

    def test_tama_return_correct_t(self):
        speech = SpeechBuilder("tama/tests/data/test.wav").speech

        calculator = Calculator(speech, frame_step=3, frame_length=4)

        T, moving_average = calculator.calculate("F0_MEAN")


        self.assertEqual([t for t in T], [3.0, 6.0, 9.0, 12.0, 15.0, 18.0])

    def test_tama_works_for_a_specified_interval(self):
        speech = SpeechBuilder("tama/tests/data/test.wav").speech

        calculator = Calculator(speech, frame_step=3, frame_length=4)

        T, moving_average = calculator.calculate("F0_MEAN", interval=Interval(0, 10))


        self.assertEqual([t for t in T], [3.0, 6.0, 9.0])
