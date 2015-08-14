#! coding:utf-8
import pandas as pd
from unittest import TestCase
from sympy import Interval
from . import interval_distance, remove_A_B_variables


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


class RemoveABVariablesTest(TestCase):
    def test_for_empty_df_it_should_keep_columns(self):
        df = pd.DataFrame(columns=["session", "task", "X"])

        remove_A_B_variables(df, new_vars=["X"], old_vars=[])

        self.assertEquals(df.columns, ["session", "task", "X"])
