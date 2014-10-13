#! coding: utf-8
from sympy import Interval

def build_utterances(word_intervals):
    """
    Given a set of word intervals, it returns a list of intervals that results from repeatedly merging adjacent intervals which are both silent or nonsilent.
    """
    current_interval = None
    speech_intervals = []

    for word_interval in word_intervals:
        if not current_interval and not word_interval.is_silent:
            current_interval = Interval(word_interval.inf, word_interval.sup)
        elif current_interval:
            if not word_interval.is_silent:
                # If it is not
                current_interval = Interval(current_interval.inf, word_interval.sup)
            # If not, push current
            else:
                speech_intervals.append(current_interval)
                current_interval = None

    if current_interval:
        speech_intervals.append(current_interval)

    return speech_intervals
