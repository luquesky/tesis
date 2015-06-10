#! coding: utf-8
from __future__ import division
import config
import pandas as pd
from calculator import Calculator
from helpers import intersecting_utterances, hybrid_intersecting_utterances
import logging

logger = logging.getLogger('main')


def tama(speech, feature, frame_step=None, frame_length=None, interpolate=False, interval=None):
    """
    Given a speech, it returns the time aligned moving average (tama) for the feature.

    Parameters
    ----------

    speech: Speech
        An object responding to utterances and length properties

    feature: string
        Any of the features that could be returned by speech.get_features()

    Returns
    -------

    T: Array
    Consisting on the time where the intervals where taken

    averages: Array
    The result of applying TAMA on the selected feature for the current interval

    """

    frame_step = frame_step or config.SERIES_FRAME_STEP
    frame_length = frame_length or config.SERIES_FRAME_LENGTH

    calculator = Calculator(
        speech,
        frame_step=frame_step,
        frame_length=frame_length,
        utterance_extractor=intersecting_utterances,
        interpolate=interpolate
    )

    return calculator.calculate(feature, interval=interval)


def normalized_tama(speech, feature, frame_step=None, frame_length=None, interpolate=False, interval=None):
    T, mean = tama(speech, feature, frame_step=frame_step, frame_length=frame_length, interpolate=interpolate, interval=interval)

    return pd.Series((T - mean) / T.std(), dtype=float)


def hybrid_tama(speech, feature, frame_step=10, frame_length=20, interpolate=False, interval=None):
    calculator = Calculator(
        speech,
        frame_step=frame_step,
        frame_length=frame_length,
        utterance_extractor=hybrid_intersecting_utterances,
        interpolate=interpolate
    )

    return calculator.calculate(feature, interval=interval)


# Calculates weighted mean in a speech of a feature
def tama_mean(speech, feature, frame_step=10, frame_length=20, interval=None, interpolate=False):
    calculator = Calculator(speech,
        frame_step=frame_step,
        frame_length=frame_length,
        utterance_extractor=intersecting_utterances,
        interpolate=interpolate
    )

    return calculator.get_average(interval, feature)


def tama_standard_error(speech, feature, frame_step=10, frame_length=20, interpolate=False):
    calculator = Calculator(speech,
        frame_step=frame_step,
        frame_length=frame_length,
        utterance_extractor=intersecting_utterances,
        interpolate=interpolate
    )
    prefix = feature.split("_")[0]
    stdv_feature = prefix + "_STDV"
    return calculator.get_standard_deviation(stdv_feature)
