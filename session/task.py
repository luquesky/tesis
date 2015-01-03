#! coding:utf-8
from sympy import Interval

# This models a task belonging to a session of Columbia Games
class Task(object):
    SILENCE_WORD = '#'

    def __init__(self, inf, sup, description):
        self.description = description
        self.interval = Interval(inf, sup)

    @property
    def inf(self):
        return self.interval.inf

    @property
    def sup(self):
        return self.interval.sup

    def intersect(self, another_interval):
        return self.interval.intersect(another_interval)


    def __eq__(self, other):
        return (self.interval == other.interval) and (self.description == other.description)

    def __str__(self):
        return "%s Task: %s" % (self.interval, self.description)

    def __repr__(self):
        return self.__str__()