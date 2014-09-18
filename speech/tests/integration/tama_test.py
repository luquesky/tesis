#! coding:utf-8
import csv
import os
from sympy import Interval
from unittest import TestCase
from ... import Speech, tama, SpeechInterval, FeatureExtractor

DATA_DIR = os.getcwd() + "/speech/tests/integration/data"

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        intervals = get_word_intervals()

        speech = Speech(speech_intervals=get_word_intervals(), feature_extractor= build_feature_extractor())
        tama(speech, frame_step=2, frame_length=4)

    # The wav we use here has 20.87 seconds =>
    # Using frame_step = 2, and frame_length = 4 => there should be 10 frames! (the last one should be chopped)

    def test_tama_returns_the_right_number_of_frames(self):
        intervals = get_word_intervals()

        speech = Speech(speech_intervals=get_word_intervals(), feature_extractor= build_feature_extractor())
        moving_average = tama(speech, frame_step=2, frame_length=4)

        self.assertEqual(len(moving_average), 10)


def get_word_intervals():
    intervals = []
    with open("speech/tests/integration/data/test.words") as test_words:
        rows = csv.reader(test_words, delimiter=" ")
        for row in rows:
            intervals.append(SpeechInterval(float(row[0]), float(row[1]),row[2]))
    return intervals

# This is quite ad hoc
def build_feature_extractor():
    return FeatureExtractor(
        path_to_script = os.getcwd() + "/scripts/extractStandardAcoustics.praat",
        path_to_praat = "/usr/local/bin/praat",
        path_to_wav= DATA_DIR + "/test.wav"
    )

