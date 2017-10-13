#! coding: utf-8
import pandas as pd
from unittest import TestCase
from .. import remove_yes_no_variables


class RemoveYesNoVariablesTest(TestCase):
    def test_for_empty_dataframe(self):
        dataframe = pd.DataFrame(columns=[])

        new_dataframe = remove_yes_no_variables(dataframe)

        self.assertEqual(len(new_dataframe.columns), 0)

    def test_for_a_dataframe_with_a_yes_variable(self):
        dataframe = pd.DataFrame({"var_yes": [1, 2, 3]})

        new_dataframe = remove_yes_no_variables(dataframe)

        self.assertItemsEqual(new_dataframe.columns, ["var"])

    def test_it_sets_the_yes_variable_into_the_unsuffixed_variable(self):
        dataframe = pd.DataFrame({"var_yes": [1, 2, 3]})

        new_dataframe = remove_yes_no_variables(dataframe)

        self.assertTrue((new_dataframe["var"] == dataframe["var_yes"]).all())

    def test_it_removes_the_no_variables(self):
        dataframe = pd.DataFrame({"var_no": [5,6,7]})

        new_dataframe = remove_yes_no_variables(dataframe)

        self.assertTrue("var_no" not in new_dataframe.columns)

