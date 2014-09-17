#! coding: utf-8
from sympy import Interval

def tama(speech, frame_step=10, frame_length=20):
    current_step = frame_step
    while current_step <= speech.length():
        frame = __get_frame_for(speech, frame_step, current_step)
        matching_intervals = __intervals_overlapping(speech, frame)
        current_step+= frame_step

def __get_frame_for(speech, step, end):
    lower_bound = max([end-step, 0])
    return Interval(lower_bound, step)

def __intervals_overlapping(speech, frame):
    return speech.intervals_overlapping(frame)
