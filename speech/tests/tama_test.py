#! coding:utf-8
from unittest import TestCase
from .. import Speech, tama

class TamaTest(TestCase):

    def test_tama_can_be_run(self):
        speech = Speech("foo")
        tama(speech)   
