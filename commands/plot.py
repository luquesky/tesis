#! coding: utf-8
import logging
import matplotlib.patches as mpatches
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
    plt.plot(TA, averagesA, c="r")
    plt.plot(TB, averagesB, c="b")

    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)

    plt.show()

def plot_autocorrelations(feature, TA, averagesA, TB, averagesB):
    lags = range(1, min(10, len(TA)))
    autocorr1 = [autocorrelation_coefficient(averagesA, lag) for lag in lags]

    autocorr2 = [autocorrelation_coefficient(averagesB, lag) for lag in lags]

    red_patch = mpatches.Patch(color='red', label='Speaker A')
    blue_patch = mpatches.Patch(color='blue', label='Speaker B')
    plt.legend(handles=[red_patch, blue_patch])

    plt.scatter(lags, autocorr1, c="red")
    plt.scatter(lags, autocorr2, c="blue")

    plt.show()

