#! coding:utf-8
UTTERANCE_THRESHOLD = 0.4

def intersecting_utterances(speech, frame):
    """
    Find all the utterances that have intersection for the frame. For utterances in the boundaries, it chops them

    This is the method used in classic tama

    Let's suppose my frame is (10s, 20s) and I have speech intervals:
    9s    10.5s 'hi'
    10.5s 19s   #
    19.5s   20.5s 'how'

    Then, the frame's matching intervals should be
    (10, 10.5), (10.5, 19) and (19, 20)
    """
    intervals = []
    for utterance in speech.utterances:
        intersection = utterance.intersect(frame)
        # Not an empty set' nor a singleton
        if intersection.measure > UTTERANCE_THRESHOLD:
            intervals.append(intersection)
    return intervals

def hybrid_intersecting_utterances(speech, frame):
    """
    Find all the utterances that have intersection for the frame. For utterances in the boundaries, it adds them completely (thus expanding the frame boundaries)
    """
    intervals = []
    for utterance in speech.utterances:
        intersection = utterance.intersect(frame)
        # Not an empty set' nor a singleton
        if intersection.measure > 0:
            intervals.append(utterance)
    return intervals


def interpolate(averages):
    for index, average in enumerate(averages):
        if average != .0:
            continue
        elif (index > 0):
            if (averages[index-1] != .0) and (averages[index+1] != .0):
                averages[index] = (averages[index-1] + averages[index+1]) / 2.0
            else:
                averages[index] = averages[index-1]

