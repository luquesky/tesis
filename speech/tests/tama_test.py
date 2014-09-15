#! coding:utf-8
from sympy import Interval
from unittest import TestCase
from .. import Speech, tama, SpeechInterval

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        speech = Speech(speech_intervals=[
            SpeechInterval(0, 14, "#"),
            SpeechInterval(14, 14.5, "hi"),
        ])
        tama(speech)   
