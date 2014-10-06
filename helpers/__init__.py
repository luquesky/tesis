#! coding:utf-8
from scipy.stats.stats import ss

# Calculates autocorrelation coefficient for X taking lag = k
def autocorrelation_coefficient(X, lag):
    xm = X.mean()
    num = sum((X[lag:] - xm) * (X[:-lag] - xm))
    denom = ss(X - xm)
    return num / denom
