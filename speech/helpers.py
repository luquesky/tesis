#! coding: utf-8
from sympy import Interval

def build_utterances(word_intervals):
    current_interval = None
    is_current_interval_silent = None
    speech_intervals = []

    for word_interval in word_intervals:
        if not current_interval:
            current_interval = Interval(word_interval.inf, word_interval.sup)
            is_current_interval_silent = word_interval.is_silent
        else:
            # If they are both silent, or both nonsilent => merge
            if bool(word_interval.is_silent) == bool(is_current_interval_silent):
                current_interval = Interval(current_interval.inf, word_interval.sup)
            # If not, push current
            else:
                speech_intervals.append(current_interval)
                current_interval = Interval(word_interval.inf, word_interval.sup)
                is_current_interval_silent = word_interval.is_silent

    if current_interval:
        speech_intervals.append(current_interval)

    return speech_intervals