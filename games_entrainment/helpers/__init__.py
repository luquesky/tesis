#! coding:utf-8
import numpy as np
import pandas as pd
from ..tsa import entrainment, cross_correlogram, autocorrelogram

from .speech import (
    create_speech,
    get_word_intervals,
    get_ctm_word_intervals,
    create_tama,
    TaskTooShort,
)


def plot_tamas(A, B, feature, ax=None):
    sp = pd.DataFrame({'A': A, 'B': B}).plot(
        color=['r', 'b'],
        style='-o',
        ax=ax
    )
    sp.set_xlabel("Time")
    sp.set_ylabel("Average %s" % feature)
    sp.set_title("Time plot")

    l_AB, E_AB, l_BA, E_BA = entrainment(A, B, lags=range(-6, 6))
    #print "A -> B = %.5f (lag = %s)" % (E_AB, l_AB)
    #print "B -> A = %.5f (lag = %s)" % (E_BA, l_BA)


def plot_cross_correlogram(A, B, feature, ax=None, max_lag=6):
    n = len(A)
    lag_limit = min(max_lag, n)
    lags = range(-lag_limit, lag_limit+1)

    cross_correlations = cross_correlogram(A, B, lags)
    sp = cross_correlations.plot(style="bo", ax=ax)
    sp.set_xlabel("Lag")
    sp.set_ylabel("Correlation")
    sp.set_title("Cross-Correlogram")

    sp.set_ylim([-1, 1])

    confidence_value = 2 / np.sqrt(n)
    # Draw confidence interval
    sp.axhline(confidence_value, linestyle='dashed', color='g')
    sp.axhline(-confidence_value, linestyle='dashed', color='g')
    # Draw axes
    sp.axvline(0, color="k")
    sp.axhline(0, color="k")
    # Draw max values
    l_AB, E_AB, l_BA, E_BA = entrainment(A, B, lags=lags)
    pd.Series({l_AB: E_AB, l_BA: E_BA}).plot(style="ro", ax=ax)


def plot_autocorrelations(A, B=None, ax=None):
    n = len(A)
    lag_limit = min(10, n/4 + 1)
    lags = range(lag_limit+1)

    autocorrA = autocorrelogram(A, lags)
    autocorrB = None
    if B is not None:
        autocorrB = autocorrelogram(B, lags)

    sp = pd.DataFrame({'A': autocorrA, 'B': autocorrB}).plot(
        color=['r', 'b'],
        style='-o',
        ax=ax
    )
    sp.set_xlabel("Lag")
    sp.set_ylabel("Autocorrelation")
    sp.set_title("Autocorrelogram")
    sp.set_ylim([-1, 1])

    confidence_value = 2 / np.sqrt(n)
    # Draw confidence interval
    sp.axhline(confidence_value, linestyle='dashed', color='g')
    sp.axhline(-confidence_value, linestyle='dashed', color='g')
    # Draw axes
    sp.axvline(0, color="k")
    sp.axhline(0, color="k")


def interval_distance(int1, int2):
    intersect = int1.closure.intersect(int2.closure)

    # If not empty =>
    if not intersect.is_EmptySet:
        return 0.0
    else:
        return min([abs(int2.inf - int1.sup), abs(int1.inf - int2.sup)])


def remove_A_B_variables(df, new_vars, old_vars):
    speaker = df['speaker']
    for sv in new_vars:
        try:
            sv_A = "%s_A" % sv
            sv_B = "%s_B" % sv
            df[sv] = (1 - speaker) * df[sv_A] + speaker * df[sv_B]
        except KeyError:
            pass
    df.drop(old_vars, axis=1, inplace=True)
