#! coding:utf-8
import numpy as np
import pandas as pd
from unittest import TestCase
from sympy import Interval
from . import autocorrelation_coefficient, interval_distance, cross_correlation

class AutocorrelationCoefficientTest(TestCase):
    def test_it_works(self):
        x = np.array([1.0, 2.0, 3.0, 4.0], dtype=float)

        self.assertAlmostEqual(autocorrelation_coefficient(x, lag=1), 0.25)

class IntervalDistanceTest(TestCase):
    def test_for_overlapping_intervals(self):
        interval1 = Interval(0, 1)
        interval2 = Interval(1, 2)
        self.assertAlmostEqual(interval_distance(interval1, interval2), .0)

    def test_for_first_interval_is_to_the_left(self):
        interval1 = Interval(0, 1)
        interval2 = Interval(2, 3)
        self.assertAlmostEqual(interval_distance(interval1, interval2), 1.0)

    def test_for_first_interval_is_to_the_right(self):
        interval1 = Interval(2, 3)
        interval2 = Interval(0, 1)
        self.assertAlmostEqual(interval_distance(interval1, interval2), 1.0)


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
