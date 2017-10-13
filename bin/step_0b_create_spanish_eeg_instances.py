#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import fire
import config
import glob
import os
import wave
import logging
import pandas as pd

logger = logging.getLogger('main')


def get_wav_duration(wav_path):
    """Return duration in seconds of wav file."""
    wav = wave.open(wav_path)

    return wav.getnframes() / wav.getframerate()


def create_instance(wav_path, phrases_dir, session_info):
    """Create instance of speech."""
    base_file = os.path.split(wav_path)[1]
    name = os.path.splitext(base_file)[0]
    split_file = name.split(".")
    words_path = os.path.join(phrases_dir, name + ".phrases")

    session = int(split_file[0][1:])
    task = int(split_file[2])
    # Convert to speaker 0 and 1
    speaker = int(split_file[3][-1]) - 1
    assert(speaker == 0 or speaker == 1)
    gender_column = "genderA" if speaker == 0 else "genderB"

    return {
        "session": session,
        "task": task,
        "wav_path": os.path.abspath(wav_path),
        "words_path": os.path.abspath(words_path),
        "speaker": speaker,
        "gender": session_info.loc[session, gender_column],
        "time_start": 0.0,
        "time_end": get_wav_duration(wav_path),
    }


class CreateInstances(object):
    """Create instances of tasks."""

    def run(self, output_path,
            wav_dir="data/games-eeg/wavs/",
            phrases_dir="data/games-eeg/annotations/phrases",
            session_info_path="data/spanish-session-info.csv"):
        """Run this command.

        Parameters
        ----------

        output_path: string
            Where to output a csv file with respective features

        wav_dir: string
            where to look for wav files

        phrases_dir: string
            where to look for .phrases files

        session_info: string
            path to .csv with
        """
        logger.info("Creating instances...")
        wavs = glob.glob(os.path.join(wav_dir, "*.wav"))

        # Exclude session 28
        wavs = [wav for wav in wavs if 's28' not in wav]

        session_info = pd.read_csv(session_info_path)
        session_info.set_index("session", inplace=True)

        features = [create_instance(wav_path, phrases_dir, session_info) for wav_path in wavs]
        df = pd.DataFrame(features)
        df.set_index(["session", "task", "speaker"], inplace=True)
        df.to_csv(output_path)

        logger.info("CSV saved to {}".format(output_path))


if __name__ == '__main__':
    fire.Fire(CreateInstances)
