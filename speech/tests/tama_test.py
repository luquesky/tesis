#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import Speech, tama

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        speech = Speech(speech_intervals=[
            (Interval(0, 14), "#"),
            (Interval(14, 14.5), "hi"),
        ])
        tama(speech)   
