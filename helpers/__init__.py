#! coding:utf-8
import pandas as pd
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
# Cross correlation is defined with the very same formula as the correlation
# but adding a lag in the indices in the numerator, which is used to compare the
# values of X and Y but with a delay. The denominator stays the same
#
#
# Positive correlation (l > 0) means that we calculate the "correlation" between
# X_lag, X_{lag+1}, ..., X_n and Y_1, ... , Y_{n-lag}
#
# If the lag < 0, then we calculate the "correlation" between
# X_1, ..., X_{n-lag}, and Y_lag, ..., Y_n
# if lag == 0, it is the same as the correlation
#
# To wrap up, if l > 0, and we have a good value (~1), it means that Y influences X. If l < 0, X influences Y. If l = 0, then we have feedback

# (see Kousidis et al[2009])


def cross_correlation(X, Y, lag):
    xm = X.mean()
    ym = Y.mean()

    if lag < 0:
        return cross_correlation(Y, X, -lag)
    elif lag == 0:
        xprod = X - xm
        yprod = Y - ym
    else:
        # Here we take...
        # x_lag, x_{lag+1}, ..., x_n and
        # y_1, y_2, ... y_lag
        xprod = X.values[lag:] - xm
        yprod = Y.values[:-lag] - ym

    # Here we use values to ignore the indices
    # .. and create a new Series to sum ignoring
    num = pd.Series(xprod * yprod).sum()
    denom = sqrt(((X - xm) ** 2).sum() * ((Y - ym) ** 2).sum())

    return num / denom


def cross_correlogram(X, Y, lags=None):
    n = len(X)

    if not lags:
        lags = range(-n/2, n/2 + 1)

    return pd.Series({lag:cross_correlation(X, Y, lag) for lag in lags})


# Returns l_XY, E_XY, l_YX, E_YX where
#  - E_XY is the maximum correlation in the negative side of the X-Y correlogram
#  - L_XY is the lag where E_XY occurs
#  - E_YX is the maximum correlation in the positive side of the X-Y correlogram
#  - L_YX is the lag where E_YX occurs
def entrainment(X, Y, lags=None):
    assert(len(X) == len(Y))
    n = len(X)

    if not lags:
        lags = range(-n/2, n/2 + 1)

    correlations = cross_correlogram(X, Y, lags=lags)
    l_xy = correlations[correlations.index <= 0].abs().idxmax()
    l_yx = correlations[correlations.index >= 0].abs().idxmax()

    return l_xy, correlations[l_xy], l_yx, correlations[l_yx]
