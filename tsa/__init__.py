#! coding:utf-8
import pandas as pd
import numpy as np
from math import sqrt
from scipy.stats.stats import ss
import config



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
#
# (see Kousidis et al[2009])
# -----------
# Parameters
# X, Y : Time Series
# lag: lag corresponding to the description above
# min_threshold: Number of points required to calculate the cross-correlation. If shifted-series have less points than this, it returns np.nan


def cross_correlation(X, Y, lag, min_threshold=None):
    min_threshold = min_threshold or config.CORRELATION_LENGTH_THRESHOLD
    xm = X.mean()
    ym = Y.mean()

    if lag < 0:
        return cross_correlation(Y, X, -lag, min_threshold=min_threshold)
    elif lag == 0:
        xprod = X - xm
        yprod = Y - ym
    else:
        # Here we take...
        # x_lag, x_{lag+1}, ..., x_n and
        # y_1, y_2, ... y_lag
        xprod = X.values[lag:] - xm
        yprod = Y.values[:-lag] - ym

    def count_not_nan(arr):
        return (~np.isnan(arr)).sum()

    # If less than min_threshold...

    if count_not_nan(xprod) < min_threshold or count_not_nan(yprod) < min_threshold:
        return np.nan

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


# Calculates autocorrelation coefficient for X taking lag = k
def autocorrelation(X, lag):
    if lag == 0:
        return 1.0

    xm = X.mean()

    num = pd.Series((X.values[lag:] - xm) * (X.values[:-lag] - xm)).sum()
    denom = pd.Series((X - xm)**2).sum()

    return num / denom


def autocorrelogram(X, lags=None):
    n = len(X)

    if not lags:
        lags = range(n/2 + 1)

    return pd.Series({lag: autocorrelation(X, lag) for lag in lags})


def autoregressive(Z, *alphas):
    X = pd.Series(index=range(len(Z)))
    for i in X.index:
        X[i] = Z[i]

        for j, alpha in enumerate(alphas):
            index = i - (j+1)

            if index > 0:
                X[i] = alpha * X[index] + Z[i]

    return X


# Returns rX, rY, residuals of X and Y
def autoregressive_prewhitening(X, Y):

    estimator_alpha = autocorrelation(X, 1)
    mu = X.mean()

    def _filter(T):
        # To sum the previous value, we have to move the series forward (and replace nans with 0!)
        T_shift = T.shift(1).replace(np.nan, 0)
        return (T - mu) - estimator_alpha * (T_shift - mu)

    rX = _filter(X)
    rY = _filter(Y)
    return rX, rY
