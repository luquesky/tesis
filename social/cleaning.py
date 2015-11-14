#! coding: utf-8
import re
import social
import pandas as pd


def __social_variables(social_dataframe):
    return filter(lambda x: x != "session" and x != "task" and x !="speaker", social_dataframe.columns)


def __variables_with_suffix(social_dataframe, suffix):
    regex = r'.*_%s' % suffix

    return filter(lambda x: re.match(regex, x), __social_variables(social_dataframe))


def remove_yes_no_variables(social_dataframe):
    no_variables = __variables_with_suffix(social_dataframe, "no")
    yes_variables = __variables_with_suffix(social_dataframe, "yes")

    # Remove
    yes_rename = {v:v[0:-4] for v in yes_variables}
    new_df = social_dataframe.rename(columns=yes_rename, inplace=False)

    new_df.drop(no_variables, axis=1, inplace=True)

    return new_df


def remove_a_b_variables(social_dataframe):
    A_df = social_dataframe.copy(deep=True)
    B_df = social_dataframe.copy(deep=True)

    A_df['speaker'] = 0
    B_df['speaker'] = 1

    ret = A_df.append(B_df)

    A_variables = __variables_with_suffix(social_dataframe, "A")
    B_variables = __variables_with_suffix(social_dataframe, "B")

    variables_without_suffix = [var[:-2] for var in A_variables]

    for var in variables_without_suffix:
        try:
            sv_A = "%s_A" % var
            sv_B = "%s_B" % var
            ret[var] = (1 - ret["speaker"]) * ret[sv_A] + ret["speaker"] * ret[sv_B]
        except KeyError:
            print "%s is not of type _A or _B"
            pass

    ret.drop(A_variables, axis=1, inplace=True)
    ret.drop(B_variables, axis=1, inplace=True)
    return ret


def get_social_variables(path):
    dataframe = pd.DataFrame.from_csv(path)
    dataframe = remove_a_b_variables(remove_yes_no_variables(dataframe))

    columns_to_be_removed = [x for x in __social_variables(dataframe) if x not in social.relevant_variables]
    dataframe.drop(columns_to_be_removed, axis=1, inplace=True)

    return dataframe
