#! coding: utf-8
from __future__ import division
import logging
import math
import numpy as np
from sympy import Interval
from helpers import interpolate, intersecting_utterances, hybrid_intersecting_utterances

INTERVAL_THRESHOLD = 0.5

logger = logging.getLogger('main')

def base_tama(speech, feature, utterance_extractor, frame_step, frame_length):
    current_step = frame_step
    T = []
    averages = []

    total_sum = __tama_sum(speech, speech.utterances, feature)


    while current_step <= speech.length():
        frame = __get_frame_for(speech, length=frame_length, middle=current_step)

        T.append(current_step)
        matching_intervals = utterance_extractor(speech, frame)
        log_frame(frame)

        average = __tama_sum(speech, matching_intervals, feature)
        averages.append(average / total_sum)
        current_step+= frame_step

    # For zero-values (for instance, those in which speaker does not has an utterance) let's interpolate values
    interpolate(averages)

    return np.array(T, dtype=float), np.array(averages, dtype=float)


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
    return base_tama(speech, feature, intersecting_utterances, frame_step=frame_step, frame_length=frame_length)

def hybrid_tama(speech, feature, frame_step=10, frame_length=20):
    return base_tama(speech, feature, hybrid_intersecting_utterances, frame_step=frame_step, frame_length=frame_length)

def __get_frame_for(speech, length, middle):
    lower_bound = middle - length/2.0
    upper_bound = middle + length/2.0
    return Interval(lower_bound, upper_bound)

def __tama_sum(speech, intervals, feature):
    # Now, for each matching interval, let's calculate the f0 mean
    # Remember that is an weighted average, where the weight of each interval is their ratio of length (against frame)
    # OBS: There might be some intervals chopped off the frame, as they might be very tiny
    sum_of_lengths = .0
    average = 0
    for interval in intervals:
        features = speech.get_features(interval)
        if math.isnan(features[feature]):
            logger.warning("Feature %s is nan in %s" % (feature,interval))
            continue
        sum_of_lengths += interval.measure
        average += features[feature] * interval.measure

        log_features(interval, features)

    if sum_of_lengths > 0:
        average = average / sum_of_lengths
    return average

def log_frame(frame):
    logger.debug("=" * 80)
    logger.debug("Frame = %s" % frame)
    logger.debug("Matching Utterances:")

def log_features(interval, features):
    logger.debug("#" * 40)
    logger.debug(interval)

    logger.debug("Features:")
    logger.debug(features)
