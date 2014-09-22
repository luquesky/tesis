#! coding: utf-8
from __future__ import division
from sympy import Interval
from helpers import intersecting_utterances, hybrid_intersecting_utterances


def tama(speech, feature, frame_step=10, frame_length=20):
    """
    Given a speech, it returns the time aligned moving average (tama) for the feature.

    Parameters
    ----------

    speech: Speech
        An object responding to utterances and length properties

    feature: string
        Any of the following features:


    """
    current_step = frame_step
    averages = []

    while current_step <= speech.length():
        frame = __get_frame_for(speech, length=frame_length, middle=current_step)
        matching_intervals = intersecting_utterances(speech, frame)

        # Now, for each matching interval, let's calculate the f0 mean
        # Remember that is an weighted average, where the weight of each interval is their ratio of length (against frame)
        # OBS: There might be some intervals chopped off the frame, as they might be very tiny
        frame_length = .0
        average = 0

        for interval in matching_intervals:
            features = speech.get_features(interval)
            print "Features for %s \n %s" % (interval, features)
            frame_length += interval.measure
            average += features[feature] * interval.measure

        average = average / frame_length
        averages.append(average )
        current_step+= frame_step

    return averages

def __get_frame_for(speech, length, middle):

    lower_bound = max([0, middle - length/2.0])
    upper_bound = min([middle + length/2.0, speech.length()])
    return Interval(lower_bound, upper_bound)
