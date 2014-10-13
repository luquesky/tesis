#! coding: utf-8
import logging
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from helpers import autocorrelation_coefficient
from tama import tama, hybrid_tama

logger = logging.getLogger('main')

def plot_tama(speech, feature, hybrid=True):
    tama_function = hybrid_tama if hybrid else tama
    T, averages = tama_function(speech, feature)

    plt.plot(T, averages)
    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)
    plt.show()

def plot_tamas(speech1, speech2, feature, hybrid=True, interpolate=True):
    tama_function = hybrid_tama if hybrid else tama
    T1, averages1 = tama_function(speech1, feature, interpolate=interpolate)
    T2, averages2 = tama_function(speech2, feature, interpolate=interpolate)

    plt.plot(T1, averages1)
    plt.plot(T2, averages2)

    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)

    corr, p = pearsonr(averages1, averages2)
    print("Pearson correlation %.5f" % corr)
    plt.show()

    lags = range(1, 10)
    autocorr1 = [autocorrelation_coefficient(averages1, lag) for lag in lags]

    autocorr2 = [autocorrelation_coefficient(averages2, lag) for lag in lags]

    plt.scatter(lags, autocorr1, c="g")
    plt.scatter(lags, autocorr2, c="r")

    plt.show()


