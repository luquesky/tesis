#! coding:utf-8
import numpy as np
import pandas as pd
from unittest import TestCase
from . import autocorrelation, cross_correlation


class AutocorrelationCoefficientTest(TestCase):
    def test_it_works(self):
        x = pd.Series([1.0, 2.0, 3.0, 4.0], dtype=float)

        self.assertAlmostEqual(autocorrelation(x, lag=1), 0.25)

    def test_it_should_return_one_for_lag_zero(self):
        X = pd.Series([1, 2, 3, 4, 5], index=range(10, 15))

        self.assertAlmostEqual(autocorrelation(X, 0), 1.0)


class CrossCorrelationTest(TestCase):
    def test_for_positive_lag(self):
        x = pd.Series([1.0, 2.0, 3.0], dtype=float)
        y = pd.Series([2, 0, 4], dtype=float)

        self.assertAlmostEqual(cross_correlation(x, y, lag=1, min_threshold=2), -0.5)

    def test_for_negative_lag(self):
        x = pd.Series([1.0, 2.0, 3.0], dtype=float)
        y = pd.Series([2, 0, 4], dtype=float)

        self.assertAlmostEqual(cross_correlation(x, y, lag=-1, min_threshold=2), 0.5)

    def test_works_with_nans(self):
        x = pd.Series([1, 2, np.nan, 3])
        y = pd.Series([2, 0, 3, 1])

        self.assertTrue(not np.isnan(cross_correlation(x, y, lag=1, min_threshold=2)))
