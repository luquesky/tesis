#! coding: utf-8
from __future__ import division
from sympy import Interval

# Tama
# Returns an array of the time series moving average
def tama(speech, feature, frame_step=10, frame_length=20):
    current_step = frame_step
    averages = []

    while current_step <= speech.length():
        frame = __get_frame_for(speech, length=frame_length, middle=current_step)
        matching_intervals = __intervals_overlapping(speech, frame)

        # Now, for each matching interval, let's calculate the f0 mean
        # Remember that is an weighted average, where the weight of each interval is their ratio of length (against frame)
        frame_length = float(frame.measure)
        average = 0

        for interval in matching_intervals:
            features = speech.get_features(interval)
            print "Features for %s \n %s" % (interval, features[feature])
            interval_ratio = float(interval.measure) / frame_length
            average += features[feature] * interval_ratio

        averages.append(average)
        current_step+= frame_step

    return averages

def __get_frame_for(speech, length, middle):

    lower_bound = max([0, middle - length/2.0])
    upper_bound = min([middle + length/2.0, speech.length()])
    return Interval(lower_bound, upper_bound)

# Find all the speech intervals that have intersection in the current frame
# Let's suppose my frame is (10s, 20s) and I have speech intervals:
# 9s    10.5s 'hi'
# 10.5s 19s   #
# 19.5s   20.5s 'how'
#
# Then, the frame's matching intervals should be
# (10, 10.5), (10.5, 19) and (19, 20)

def __intervals_overlapping(speech, frame):
    return speech.intervals_overlapping(frame)
