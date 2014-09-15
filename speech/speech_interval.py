#! coding:utf-8
from sympy import Interval

class SpeechInterval(Interval):
    def __init__(self, inf, sup, word, *args, **kwargs):
        self.word = word
        super(SpeechInterval, self).__init__(inf, sup, *args, **kwargs)
