#! coding:utf-8
from __future__ import division
import logging
import math
import numpy as np
from sympy import Interval
from helpers import interpolate, intersecting_utterances, hybrid_intersecting_utterances

logger = logging.getLogger('main')

class Calculator(object):
    def __init__(self, speech, frame_step, frame_length, utterance_extractor=None):
        self.speech = speech
        self.frame_step = frame_step
        self.frame_length = frame_length
        self.utterance_extractor = utterance_extractor or hybrid_intersecting_utterances

    def calculate(self, feature):
        current_step = self.frame_step
        T = []
        averages = []

        total_sum = self.__tama_sum(self.speech.utterances, feature)

        while current_step <= self.speech.length():
            frame = self.__get_frame_for(length=self.frame_length, middle=current_step)

            T.append(current_step)
            matching_intervals = self.utterance_extractor(self.speech, frame)
            log_frame(frame)

            average = self.__tama_sum(matching_intervals, feature)
            averages.append(average / total_sum)
            current_step+= self.frame_step

        # For zero-values (for instance, those in which speaker does not has an utterance) let's interpolate values
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
            if math.isnan(features[feature]):
                logger.warning("Feature %s is nan in %s" % (feature,interval))
                continue
            sum_of_lengths += interval.measure
            average += features[feature] * interval.measure

            log_features(interval, features)

        if sum_of_lengths > 0:
            average = average / sum_of_lengths
        return average

    def __get_frame_for(self, length, middle):
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