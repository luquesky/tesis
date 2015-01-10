#! coding:utf-8
from math import sqrt
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

# Computes the cross correlation for X, Y, and lag
# (see Kousidis et al[2009])
def cross_correlation(X, Y, lag):
    xm = X.mean()
    ym = Y.mean()

    if lag >= 0:
        # Here we take...
        # x_lag, x_{lag+1}, ..., x_n and
        # y_1, y_2, ... y_lag
        xprod = X[lag:] - xm
        yprod = Y[:-lag] - ym
    else:
        # x_1, x_2, ..., x_lag and
        # y_lag, y_{lag+1}, ... y_n
        xprod = X[:lag] - xm
        yprod = Y[-lag:] - ym

    num = sum(xprod * yprod)
    denom = sqrt(ss(X - xm) * ss(Y-ym))
    return num / denom
