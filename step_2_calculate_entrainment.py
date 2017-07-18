#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import pandas as pd
import config
import logging
import fire
from tsa import entrainment


logger = logging.getLogger('main')


def calculate_entrainments(df, feature):
    """Calculate entrainments."""
    a_speaker_rows = df[df.speaker == 0]
    tama_column = "{}_tama".format(feature)
    entrainment_column = "{}_entrainment".format(entrainment)
    best_lag_column = "{}_best_lag".format(entrainment)

    df[entrainment_column] = None
    df[best_lag_column] = None

    for a_index, a_speech_row in a_speaker_rows.iterrows():
        b_index = ((df.session == a_speech_row.session) & (df.task == a_speech_row.task) & (df.speaker == 1)).idxmax()

        b_speech_row = df.iloc[b_index]

        A, B = a_speech_row[tama_column], b_speech_row[tama_column]
        l_AB, E_AB, l_BA, E_BA = entrainment(A, B, lags=range(-6, 6))

        df.loc[a_index, entrainment_column] = E_AB
        df.loc[a_index, best_lag_column] = l_AB
        df.loc[b_index, entrainment_column] = E_BA
        df.loc[b_index, best_lag_column] = l_BA




class CalculateEntrainments(object):
    """Calculate entrainments for AP variables."""

    def run(self, pickle_path, features=None):
        """Run the command.

        Parameters:
        -----------

        pickle: string
            Path to input pickle
        """
        df = pd.read_pickle(pickle_path)
        features = features or ["F0_MEAN"]

        for feature in features:
            calculate_entrainments(df, feature)


if __name__ == '__main__':
    fire.Fire(CalculateEntrainments)
