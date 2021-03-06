#! coding:utf-8
# This models a task belonging to a session of Columbia Games


class Task(object):
    SILENCE_WORD = '#'

    def __init__(self, interval, speechA, speechB, number, name="", description=""):
        self.description = description
        self.speechA = speechA
        self.speechB = speechB
        self.name = name
        self.number = int(number)
        self.interval = interval

    @property
    def inf(self):
        return self.interval.inf

    @property
    def sup(self):
        return self.interval.sup

    @property
    def length(self):
        return self.sup - self.inf

    def intersect(self, another_interval):
        return self.interval.intersect(another_interval)

    def __eq__(self, other):
        return (self.interval == other.interval) and (self.description == other.description)

    def __str__(self):
        return "%s Task: %s" % (self.interval, self.description)

    def __repr__(self):
        return self.__str__()
