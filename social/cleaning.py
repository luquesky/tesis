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

def remove_a_b_variables(social_dataframe):
    A_df = social_dataframe.copy(deep=True)
    B_df = social_dataframe.copy(deep=True)

    A_df['speaker'] = 0
    B_df['speaker'] = 1

    ret = A_df.append(B_df)
    # speaker = df['speaker']
    # for sv in new_vars:
    #     try:
    #         sv_A = "%s_A" % sv
    #         sv_B = "%s_B" % sv
    #         df[sv] = (1 - speaker) * df[sv_A] + speaker * df[sv_B]
    #     except KeyError:
    #         print "%s is not of type _A or _B"
    #         pass
    # df.drop(old_vars, axis=1, inplace=True)
    return ret