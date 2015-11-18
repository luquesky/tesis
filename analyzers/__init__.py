#! coding:utf-8
import pandas as pd
import social
from analyzer import Analyzer


def correlation_analysis(df, entrainment_var="entrainment"):
    corr = pd.Series(index=social.relevant_variables)

    for var in social.relevant_variables:
        corr[var] = df[entrainment_var].corr(df[var])

    return corr
