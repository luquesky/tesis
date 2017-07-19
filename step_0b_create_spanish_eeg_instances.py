#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import fire
import config
import glob
import os
import logging
import pandas as pd

logger = logging.getLogger('main')


def create_instance(wav_path, phrases_dir):
    """Create instance of speech."""

    base_file = os.path.split(wav_path)[1]
    name = os.path.splitext(base_file)[0]
    split_file = name.split(".")
    words_path = os.path.join(phrases_dir, name + ".phrases")

    session = int(split_file[0][1:])
    task = int(split_file[2])
    # Convert to speaker 0 and 1
    speaker = int(split_file[3][-1]) - 1

    return {
        "session": session,
        "task": task,
        "wav_path": wav_path,
        "speaker": speaker,
        "words_path": words_path,
        "time_start": 0.0,
        "time_end": float("+inf")
    }


class CreateInstances(object):
    """Create instances of tasks."""

    def run(self, output_path, wav_dir="data/games-eeg/wavs/", phrases_dir="data/games-eeg/annotations/phrases"):
        """Run this command.

        Parameters
        ----------

        output_path: string
            Where to output a csv file with respective features

        wav_path: string
            path to wav files

        """
        logger.info("Creating instances...")
        wavs = glob.glob(os.path.join(wav_dir, "*.wav"))
        features = [create_instance(wav_path, phrases_dir) for wav_path in wavs]

        df = pd.DataFrame(features)
        df.set_index(["session", "task", "speaker"], inplace=True)

        df.to_csv(output_path)

        logger.info("CSV saved to {}".format(output_path))


if __name__ == '__main__':
    fire.Fire(CreateInstances)
