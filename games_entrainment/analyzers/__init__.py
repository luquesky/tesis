#! coding:utf-8
import pandas as pd
import social
from analyzer import Analyzer


def correlation_analysis(df, entrainment_var="entrainment", social_vars=None):

    social_vars = social_vars or social.relevant_variables

    corr = pd.Series(index=social_vars)

    for var in social_vars:
        corr[var] = df[entrainment_var].corr(df[var])

    return corr
