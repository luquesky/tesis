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

UTTERANCE_THRESHOLD = 0.4

def intersecting_utterances(speech, frame):
    """
    Find all the utterances that have intersection for the frame. For utterances in the boundaries, it chops them

    This is the method used in classic tama

    Let's suppose my frame is (10s, 20s) and I have speech intervals:
    9s    10.5s 'hi'
    10.5s 19s   #
    19.5s   20.5s 'how'

    Then, the frame's matching intervals should be
    (10, 10.5), (10.5, 19) and (19, 20)
    """
    intervals = []
    for utterance in speech.utterances:
        intersection = utterance.intersect(frame)
        # Not an empty set' nor a singleton
        if intersection.measure > UTTERANCE_THRESHOLD:
            intervals.append(intersection)
    return intervals

def hybrid_intersecting_utterances(speech, frame):
    """
    Find all the utterances that have intersection for the frame. For utterances in the boundaries, it adds them completely (thus expanding the frame boundaries)
    """
    intervals = []
    for utterance in speech.utterances:
        intersection = utterance.intersect(frame)
        # Not an empty set' nor a singleton
        if intersection.measure > 0:
            intervals.append(utterance)
    return intervals
