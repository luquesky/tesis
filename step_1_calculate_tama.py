#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import fire
import csv
import os
import sympy
from games_entrainment import config
import logging
import pandas as pd
from games_entrainment.tama import tama, normalize
from games_entrainment.speech import Speech, WordInterval
from games_entrainment.speech.features import StandardAcousticsExtractor, VoiceAnalysisExtractor, CompositeExtractor, CachedExtractor

logger = logging.getLogger('main')


class TaskTooShort(Exception):
    u"""Exception for short task."""

    pass


def get_word_intervals(path_to_words, task_interval):
    """Get word intervals for a task."""
    word_intervals = []
    with open(path_to_words) as test_words:
        # Get dialect
        dialect = csv.Sniffer().sniff(test_words.read(1024))
        test_words.seek(0)
        rows = csv.reader(test_words, dialect)

        for row in rows:
            """Search for intervals in current task."""
            wint = WordInterval(float(row[0]), float(row[1]), row[2])
            if wint.inf > task_interval.sup:
                break

            intersection = task_interval.intersect(wint.interval)
            if intersection.measure > 0:
                word_intervals.append(wint)

    return word_intervals


def build_extractor(speech_row):
    """Build acoustic extractor for given speech."""
    extractor1 = StandardAcousticsExtractor(speech_row.wav_path, speech_row.gender)
    extractor2 = VoiceAnalysisExtractor(speech_row.wav_path, speech_row.gender)

    return CachedExtractor(CompositeExtractor(extractor1, extractor2))


def create_speech(speech_row):
    """Create Speech object out of a CSV Row."""
    interval = sympy.Interval(speech_row.time_start, speech_row.time_end)
    extractor = build_extractor(speech_row)
    word_intervals = get_word_intervals(speech_row.words_path, interval)

    return Speech(
        path_to_wav=speech_row.wav_path,
        interval=interval,
        word_intervals=word_intervals,
        gender=speech_row.gender,
        feature_extractor=extractor,
    )


def create_tama(speech, feature):
    """Create tama for speech and feature."""
    A, meanA = tama(speech, feature)
    normalized = normalize(A, meanA)

    if (A.count() < config.SERIES_LENGTH_THRESHOLD):
        raise TaskTooShort("Series too short")
    return normalized


def add_tamas(df, feature):
    """Add tamas to DataFrame."""
    logger.info("Building TAMAS for {}".format(feature))
    column_name = "{}_tama".format(feature)
    # I do this in such a horrible way because if I use df.apply
    # pandas tries to convert into Series of the same length
    df[column_name] = None

    for index, speech_row in df.iterrows():
        logger.info(
            "Calculating TAMA for Session {} Task {} Speaker {}".format(
                speech_row.session,
                speech_row.task,
                speech_row.speaker,
            )
        )
        try:
            normalized_tama = create_tama(speech_row.speech, feature)
            df.set_value(index, column_name, normalized_tama)
        except TaskTooShort:
            continue


class CalculateTama(object):
    """Calculate entrainments for AP variables."""

    def run(self, csv_path, output_path=None, features=None):
        """Run the command.

        Parameters:
        -----------

        csv_path: string
            Path to input csv.
        output_path: string
            Path to pickle output. Defaults to csv_path with its extension changed to .pickle
        features: list of strings
            List of features.
        """
        logger.info("Reading speeches from {}".format(csv_path))
        df = pd.read_csv(csv_path)

        df["speech"] = df.apply(create_speech, axis=1)

        features = features or config.FEATURES

        base, ext = os.path.splitext(csv_path)
        output_path = output_path or "{}.pickle".format(base)

        for feature in features:
            add_tamas(df, feature)

        df.to_pickle(output_path)

        logger.info("Pickle saved to {}".format(output_path))

if __name__ == '__main__':
    fire.Fire(CalculateTama)
