#! coding:utf-8
from sympy import Interval
# This class represents a word interval, which is simply an interval with a word.
# Special case to be mentioned, SILENCE_WORD string means silence in that interval

class WordInterval(object):
    SILENCE_WORD = '#'

    def __init__(self, inf, sup, word):
        self.word = word
        self.interval = Interval(inf, sup)

    @property
    def is_silent(self):
        return self.word == WordInterval.SILENCE_WORD

    @property
    def inf(self):
        return self.interval.inf

    @property
    def sup(self):
        return self.interval.sup

    def intersect(self, another_interval):
        return self.interval.intersect(another_interval)


    def __eq__(self, other):
        return (self.interval == other.interval) and (self.word == other.word)

    def __str__(self):
        return "%s -> %s" % (self.interval, self.word)

    def __repr__(self):
        return self.__str__()