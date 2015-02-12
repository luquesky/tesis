#! coding:utf-8
from __future__ import division
import logging
import math
import numpy as np
from sympy import Interval
from helpers import interpolate, hybrid_intersecting_utterances

logger = logging.getLogger('main')

Interval
class Calculator(object):
    def __init__(self, speech, frame_step, frame_length, utterance_extractor=None, interpolate = True):
        self.speech = speech
        self.frame_step = frame_step
        self.frame_length = frame_length
        self.utterance_extractor = utterance_extractor or hybrid_intersecting_utterances

        # This variable is set to true if, after a run, feature was undefined for a frame
        self.undefined_features = False
        self.interpolate = interpolate

    # Calculates timeline for feature
    # Returns T, Y, two equally sized numpy arrays where
    # T[i] contains the time where frame were selected
    # Y[i] contains the average of feature for that frame

    def calculate(self, feature, interval=None):
        if interval is None:
            interval = Interval(0, self.speech.length)

        current_step = interval.inf + self.frame_step
        T = []
        averages = []

        total_average = self.get_total_average(interval, feature)

        while interval.contains(current_step):
            frame = get_frame_for(length=self.frame_length, middle=current_step)

            T.append(current_step)
            matching_intervals = self.utterance_extractor(self.speech, frame)
            log_frame(frame)

            average = self.__tama_sum(matching_intervals, feature)
            averages.append(average/total_average)
            current_step+= self.frame_step

        # For zero-values (for instance, those in which speaker does not has an utterance) let's interpolate values
        if self.interpolate:
            interpolate(averages)

        return np.array(T, dtype=float), np.array(averages, dtype=float)



    def __tama_sum(self, intervals, feature):
        # Now, for each matching interval, let's calculate the f0 mean
        # Remember that is an weighted average, where the weight of each interval is their ratio of length (against frame)
        # OBS: There might be some intervals chopped off the frame, as they might be very tiny
        sum_of_lengths = .0
        average = 0
        for interval in intervals:
            features = self.speech.get_features(interval)
            if not features.has_key(feature) or math.isnan(features[feature]):
                self.undefined_features = True
                logger.debug("Feature %s is nan in %s" % (feature,interval))
                continue

            sum_of_lengths += interval.measure
            average += features[feature] * interval.measure

            log_features(interval, features)

        if sum_of_lengths > 0:
            average = average / sum_of_lengths
        return average

    def get_total_average(self, interval, feature):
        # To calculate the total average, let's find first the matching intervals...
        matching_intervals = self.utterance_extractor(self.speech, interval)
        return self.__tama_sum(matching_intervals, feature)



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