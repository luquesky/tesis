#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import fire
import csv
import sympy
import config
import logging
import pandas as pd
from speech import Speech, WordInterval

logger = logging.getLogger('main')


def get_word_intervals(path_to_words, task_interval):
    """Get word intervals for a task."""
    word_intervals = []
    with open(path_to_words) as test_words:
        rows = csv.reader(test_words, delimiter=" ")
        for row in rows:
            """Search for intervals in current task."""
            wint = WordInterval(float(row[0]), float(row[1]), row[2])
            if wint.inf > task_interval.sup:
                break

            intersection = task_interval.intersect(wint.interval)
            if intersection.measure > 0:
                word_intervals.append(wint)

    return word_intervals


def create_speech(speech_row):
    """Create Speech object out of a CSV Row."""
    logger.info(
        "Session {} Task {} Speaker {}".format(
            speech_row.session,
            speech_row.task,
            speech_row.speaker,
        )
    )

    interval = sympy.Interval(speech_row.time_start, speech_row.time_end)

    word_intervals = get_word_intervals(speech_row.words_path, interval)

    return Speech(
        path_to_wav=speech_row.wav_path,
        interval=interval,
        word_intervals=word_intervals
    )


class CalculateEntrainments(object):
    """Calculate entrainments for AP variables."""

    def run(self, csv_path=config.OUTPUT_PATH):
        """Foo."""
        logger.info("Reading speeches from {}".format(csv_path))
        df = pd.read_csv(csv_path)

        df["speech"] = df.apply(create_speech, axis=1)


if __name__ == '__main__':
    fire.Fire(CalculateEntrainments)
