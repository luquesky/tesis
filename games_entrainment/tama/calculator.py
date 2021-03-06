#! coding:utf-8
from __future__ import division
import logging
import math
import numpy as np
import pandas as pd
from sympy import Interval
from .helpers import interpolate, hybrid_intersecting_utterances

logger = logging.getLogger('main')


class Calculator(object):
    def __init__(self, speech, frame_step, frame_length, utterance_extractor=None, interpolate=False):
        self.speech = speech
        self.frame_step = frame_step
        self.frame_length = frame_length
        self.utterance_extractor = utterance_extractor or hybrid_intersecting_utterances

        # This variable is set to true if, after a run, feature was undefined for a frame
        self.undefined_features = False
        self.interpolate = interpolate

    # Calculates timeline for feature
    # Returns s, mu where
    # s is a pd.Series containing the time series
    # mu is the mean estimator (don't confuse it with sample mean)
    def calculate(self, feature, interval=None):
        if interval is None:
            interval = self.speech.interval

        current_step = interval.inf + self.frame_step
        T = []
        averages = []

        mu = self.get_average(interval, feature)

        # A frame is the time span which is taken into account when calculating the value for the time series in the current point

        while interval.contains(current_step):
            frame = get_frame_for(length=self.frame_length, middle=current_step)

            T.append(current_step)
            log_frame(frame)

            average = self.get_average(frame, feature)
            averages.append(average)
            current_step += self.frame_step

        # For zero-values (for instance, those in which speaker does not has an utterance) let's interpolate values
        if self.interpolate:
            interpolate(averages)

        series = pd.Series(np.array(averages, dtype=float), index=np.array(T, dtype=float))

        return series, mu

    def get_average(self, interval, feature):
        # To calculate the total average, let's find first the matching intervals...
        matching_intervals = self.utterance_extractor(self.speech, interval)
        return self.__tama_sum(matching_intervals, feature)

    # Calculates the standard error estimation
    # feature: A feature that calculates the S.E of a frame
    def get_standard_deviation(self, feature, frame=None):
        if not frame:
            frame = self.speech.interval

        matching_utterances = self.utterance_extractor(self.speech, frame)

        variance = 0.0

        # Sum of lengths of all utterances
        D = sum(utterance.measure for utterance in matching_utterances)

        for utterance in matching_utterances:
            w = utterance.measure / D
            # Here, we are supposed to be receiving a
            f = self.get_feature(feature, utterance)

            if math.isnan(f):
                # Ignore this interval
                continue

            variance += (w ** 2) * (f ** 2)

        return math.sqrt(variance)

    # Calculate the tama average for the feature, for given intervals
    # Remember that is an weighted average, where the weight of each interval is their ratio of length (against frame)
    # OBS: There might be some intervals chopped off the frame, as they might be very tiny
    def __tama_sum(self, intervals, feature):
        sum_of_lengths = .0
        average = 0
        for interval in intervals:
            f = self.get_feature(feature, interval)

            if math.isnan(f):
                # Ignore this interval
                continue

            sum_of_lengths += interval.measure
            average += f * interval.measure

        if sum_of_lengths > 0:
            average = average / sum_of_lengths
        else:
            average = np.nan
        return average

    def get_feature(self, feature, interval):
        f = self.speech.get_feature(feature, interval)

        if math.isnan(f):
            # Ignore this interval
            self.undefined_features = True
            logger.debug("Feature %s is nan in %s" % (feature,interval))
        return f


def get_frame_for(length, middle):
    lower_bound = middle - length/2.0
    upper_bound = middle + length/2.0
    return Interval(lower_bound, upper_bound)

def log_frame(frame):
    logger.debug("=" * 80)
    logger.debug("Frame = %s" % frame)
    logger.debug("Matching Utterances:")

def log_features(interval, features):
    logger.debug("#" * 40)
    logger.debug(interval)

    logger.debug("Features:")
    logger.debug(features)
