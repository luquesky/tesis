#! coding: utf-8
import logging
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

from speech import tama, hybrid_tama

logger = logging.getLogger('main')

def plot_tama(speech, feature, hybrid=True):
    tama_function = hybrid_tama if hybrid else tama
    T, averages = tama_function(speech, feature)

    plt.plot(T, averages)
    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)
    plt.show()

def plot_tamas(speech1, speech2, feature, hybrid=True):
    tama_function = hybrid_tama if hybrid else tama
    T1, averages1 = tama_function(speech1, feature)
    T2, averages2 = tama_function(speech2, feature)

    plt.plot(T1, averages1)
    plt.plot(T2, averages2)

    plt.xlabel("Time")
    plt.ylabel("Average %s" % feature)

    corr, p = pearsonr(averages1, averages2)
    logger.info("Pearson correlation %.5f" % corr)
    plt.show()
