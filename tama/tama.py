#! coding: utf-8
from __future__ import division
from calculator import Calculator
from helpers import intersecting_utterances, hybrid_intersecting_utterances
import logging

logger = logging.getLogger('main')


def tama(speech, feature, frame_step=10, frame_length=20):
    """
    Given a speech, it returns the time aligned moving average (tama) for the feature.

    Parameters
    ----------

    speech: Speech
        An object responding to utterances and length properties

    feature: string
        Any of the following features:

    Returns
    -------

    T: Array
    Consisting on the time where the intervals where taken

    averages: Array
    The result of applying TAMA on the selected feature for the current interval

    """
    calculator = Calculator(speech, frame_step=frame_step, frame_length=frame_length, utterance_extractor= intersecting_utterances)

    return calculator.calculate(feature)

def hybrid_tama(speech, feature, frame_step=10, frame_length=20):
    calculator = Calculator(speech, frame_step=frame_step, frame_length=frame_length, utterance_extractor= hybrid_intersecting_utterances)

    return calculator.calculate(feature)
