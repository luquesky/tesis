#! coding:utf-8
import csv
from sympy import Interval
from unittest import TestCase
from ... import Speech, tama, SpeechInterval

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        intervals = get_word_intervals()

        speech = Speech(speech_intervals=[
            SpeechInterval(0, 14, "#"),
            SpeechInterval(14, 14.5, "hi"),
        ])
        tama(speech)


def get_word_intervals():
    intervals = []
    with open("speech/tests/integration/data/test.words") as test_words:
        rows = csv.reader(test_words, delimiter=" ")
        for row in rows:
            intervals.append(SpeechInterval(float(row[0]), float(row[1]),row[2]))
