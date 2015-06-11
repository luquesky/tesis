#! coding:utf-8


def interval_distance(int1, int2):
    intersect = int1.closure.intersect(int2.closure)

    # If not empty =>
    if not intersect.is_EmptySet:
        return 0.0
    else:
        return min([abs(int2.inf - int1.sup), abs(int1.inf - int2.sup)])
