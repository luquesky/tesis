#! coding:utf-8
from sympy import Interval

class SpeechInterval(object):
    def __init__(self, inf, sup, word):
        self.word = word
        self.interval = Interval(inf, sup)

    # Delegate missing attributes to interval
    def __getattr__(self, name):
        return getattr(self.interval, name)

    def __eq__(self, other):
        return (self.interval == other.interval) and (self.word == other.word)
