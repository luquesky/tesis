#! coding:utf-8
import math
import numpy as np
from mock import Mock
from sympy import Interval
from unittest import TestCase
from speech import SpeechBuilder
from tama import Calculator
from . import build_speech

class CalculatorTest(TestCase):
    # The wav we use here has 20.87 seconds =>
    # Using frame_step = 2, and frame_length = 4 => there should be 10 frames! (the last one should be chopped)

    def test_tama_returns_the_right_number_of_frames(self):
        speech = build_speech()

        calculator = Calculator(speech, frame_step=3, frame_length=4)

        series, mean = calculator.calculate("F0_MEAN")

        self.assertEqual(len(series), 10)

    def test_tama_return_correct_t(self):
        speech = build_speech()

        calculator = Calculator(speech, frame_step=3, frame_length=4)

        series, mean = calculator.calculate("F0_MEAN")

        self.assertTrue((series.index == [3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0]).all())

    def test_tama_works_for_a_specified_interval(self):
        speech = build_speech()

        calculator = Calculator(speech, frame_step=3, frame_length=4)

        # Be careful. Not going to work for a silent interval
        series, mean = calculator.calculate("F0_MEAN", interval=Interval(13, 20))

        self.assertTrue((series.index == [16.0, 19.0]).all())


    ##
    ## Average test
    ## TODO: Refactor this...it's plainly horrible
    def test_it_calculates_the_right_average(self):
        speech = Mock()
        speech.get_feature.side_effect = [0.5, 1.25]
        utterance_extractor = Mock(return_value=[Interval(0,1), Interval(2, 4)])
        calculator = Calculator(speech, utterance_extractor=utterance_extractor, frame_step=10, frame_length=20)


        average = calculator.get_average(interval=Interval(0, 3), feature="F0_MEAN")

        self.assertAlmostEqual(average, 1.0)

class StandardDeviationTest(TestCase):
    def test_it_calculates_the_right_deviation(self):
        speech = Mock()
        speech.get_feature.side_effect = [2, 4]
        utterance_extractor = Mock(return_value=[Interval(0, 0.5), Interval(2, 2.5)])

        calculator = Calculator(speech, utterance_extractor=utterance_extractor, frame_step=10, frame_length=20)

        deviation = calculator.get_standard_deviation(feature="F0_MEAN")

        self.assertAlmostEqual(deviation, math.sqrt(5))

