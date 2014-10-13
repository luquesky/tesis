#! coding:utf-8
from scipy.stats.stats import ss

# Calculates autocorrelation coefficient for X taking lag = k
def autocorrelation_coefficient(X, lag):
    xm = X.mean()
    num = sum((X[lag:] - xm) * (X[:-lag] - xm))
    denom = ss(X - xm)
    return num / denom

def interval_distance(int1, int2):
    intersect = int1.closure.intersect(int2.closure)

    # If not empty =>
    if not intersect.is_EmptySet:
        return 0.0
    else:
        return min([abs(int2.inf - int1.sup), abs(int1.inf - int2.sup)])