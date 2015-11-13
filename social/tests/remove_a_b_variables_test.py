#! coding: utf-8
import pandas as pd
from unittest import TestCase
from .. import remove_a_b_variables


class RemoveABVariablesTest(TestCase):
    def test_for_empty_dataframe(self):
        dataframe = pd.DataFrame(columns=["session", "task"])

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertItemsEqual(new_dataframe.columns, ["session", "task", "speaker"])


    def test_for_a_var_without_suffix(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var": 2}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertEqual(new_dataframe.shape[0], 2)