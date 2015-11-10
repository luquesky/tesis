#! coding: utf-8
import re

def __variables_with_suffix(social_dataframe, suffix):
    regex = r'.*_%s' % suffix
    variables = filter(lambda x: x != "session" and x!= "task", social_dataframe.columns)

    return filter(lambda x: re.match(regex, x), variables)

def remove_yes_no_variables(social_dataframe):
    no_variables = __variables_with_suffix(social_dataframe, "no")
    yes_variables = __variables_with_suffix(social_dataframe, "yes")

    # Remove
    yes_rename = {v:v[0:-4] for v in yes_variables}
    new_df = social_dataframe.rename(columns=yes_rename, inplace=False)

    new_df.drop(no_variables, axis=1, inplace=True)

    return new_df