#! coding:utf-8
from mock import patch, mock_open, MagicMock
from unittest import TestCase
from .. import Speech

class SpeechTest(TestCase):

    def setUp(self):
        pass

    def test_length_returns_length_of_the_speech(self):
        speech = Speech(intervals=[
            (0, 14, "#"),
            (14, 14.5, "hi")
        ])
        self.assertEqual(speech.length(), 14.5)
