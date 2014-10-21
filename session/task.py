#! coding:utf-8
from sympy import Interval

# This models a task belonging to a session of Columbia Games
class Task(object):
    SILENCE_WORD = '#'

    def __init__(self, inf, sup, description):
        self.description = description
        self.interval = Interval(inf, sup)

    # Delegate missing attributes to interval
    def __getattr__(self, name):
        return getattr(self.interval, name)

    def __str__(self):
        return "%s Task: %s" % (self.interval, self.description)

    def __repr__(self):
        return self.__str__()