#! coding: utf-8
import pandas as pd
from unittest import TestCase
from .. import remove_a_b_variables


class RemoveABVariablesTest(TestCase):
    def test_for_empty_dataframe(self):
        dataframe = pd.DataFrame(columns=["session", "task"])

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertItemsEqual(new_dataframe.columns, ["session", "task", "speaker"])


    def test_for_a_row_it_should_create_two(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var": 2}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertEqual(new_dataframe.shape[0], 2)

    def test_for_a_row_it_should_create_column_speaker(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var": 2}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertItemsEqual(new_dataframe['speaker'], [0, 1])

    def test_for_a_row_it_should_preserve_unsuffixed_var(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var": 2}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertItemsEqual(new_dataframe['var'], [2, 2])

    def test_for_a_row_with_a_suffixed_variable(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var_A": 10, "var_B": 20}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertTrue((new_dataframe["var"][new_dataframe.speaker == 0] == 10).all)
        self.assertTrue((new_dataframe["var"][new_dataframe.speaker == 1] == 20).all)


    def test_it_removes_suffixed_variables(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var_A": 10, "var_B": 20}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertTrue("var_A" not in new_dataframe.columns)
        self.assertTrue("var_B" not in new_dataframe.columns)

    def test_it_keeps_other_variables(self):
        dataframe = pd.DataFrame([
            {"session": 1, "task": 1, "var_A": 10, "var_B": 20, "other_variable": 50}
        ], dtype=float)

        new_dataframe = remove_a_b_variables(dataframe)

        self.assertTrue("other_variable" in new_dataframe.columns)
