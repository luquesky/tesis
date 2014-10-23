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

def plot_tamas(feature, TA, averagesA, TB, averagesB):
    plt.plot(TA, averagesA)
    plt.plot(TB, averagesB)

    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)

    plt.show()

    lags = range(1, 10)
    autocorr1 = [autocorrelation_coefficient(averagesA, lag) for lag in lags]

    autocorr2 = [autocorrelation_coefficient(averagesB, lag) for lag in lags]

    plt.scatter(lags, autocorr1, c="g")
    plt.scatter(lags, autocorr2, c="r")

    plt.show()

