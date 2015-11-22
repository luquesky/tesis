#! coding:utf-8
import pandas as pd
import social
from analyzer import Analyzer


def correlation_analysis(df, entrainment_var="entrainment", social_vars=None):

    social_vars = social_vars or social.relevant_variables

    corr = pd.Series(index=social_vars)

    for var in social_vars:
        try:
            corr[var] = df[entrainment_var].corr(df[var])
        except KeyError as e:
            import ipdb; ipdb.set_trace()

    return corr
