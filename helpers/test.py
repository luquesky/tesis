#! coding:utf-8
import numpy as np
from unittest import TestCase
from . import autocorrelation_coefficient

class AutocorrelationCoefficientTest(TestCase):
    def test_it_works(self):
        x = np.array([1.0, 2.0, 3.0, 4.0], dtype=float)

        self.assertAlmostEqual(autocorrelation_coefficient(x, lag=1), 0.25)
