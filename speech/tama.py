#! coding: utf-8
from sympy import Interval

def tama(speech, frame_step=10, frame_length=20):
    current_step = frame_step
    while current_step <= speech.length():
        frame = __get_frame_for(speech, frame_step, current_step)
        # Now, I find all the speech intervals that have intersection in the current frame
        # Let's suppose my frame is (10s, 20s) and I have speech intervals:
        # 9s    10.5s 'hi'
        # 10.5s 19s   #
        # 19.5s   20.5s 'how'
        # 
        # Then, the frame's matching intervals should be
        # (10, 10.5), (10.5, 19) and (19, 20)
        matching_intervals = __intervals_overlapping(speech, frame)

        # Now, for each matching interval, let's calculate the f0 mean
        for interval in matching_intervals:
            speech.get_feature("f0", interval)

        current_step+= frame_step

def __get_frame_for(speech, step, end):
    lower_bound = max([end-step, 0])
    return Interval(lower_bound, step)

def __intervals_overlapping(speech, frame):
    return speech.intervals_overlapping(frame)
