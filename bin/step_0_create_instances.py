#! coding: utf-8
"""Step 0 de mi tesis."""
from __future__ import division, print_function
import fire
import sys
import os
sys.path.insert(0, os.path.abspath("."))
from games_entrainment import config
import logging
import pandas as pd
from games_entrainment.session import load_session

logger = logging.getLogger('main')


def extract_features(speech, task, session):
    """Extract features from (speech, task, session)."""
    _, wav_relpath = os.path.split(speech.path_to_wav)
    speaker_letter = wav_relpath.split(".")[3]
    speaker_num = {'A': 0, 'B': 1}[speaker_letter]

    filename, extension = os.path.splitext(speech.path_to_wav)
    path_to_words = "%s.words" % filename

    return {
        "session": session.number,
        "task": task.number,
        "task_path": session.path_to_tasks,
        "wav_path": speech.path_to_wav,
        "words_path": path_to_words,
        "speaker": speaker_num,
        "gender": speech.gender,
        "time_start": speech.interval.inf,
        "time_end": speech.interval.sup,
    }


class CreateInstances(object):
    """Create instances of tasks."""

    def run(self, output_path=config.OUTPUT_PATH):
        """Foo."""
        features = []

        logger.info("Creating instances...")
        for session_no in range(1, 13):
            session = load_session(session_no)
            for task in session.tasks:
                for speech in [task.speechA, task.speechB]:
                    features.append(extract_features(speech, task, session))

        df = pd.DataFrame(features)
        df.set_index(["session", "task", "speaker"], inplace=True)
        df.to_csv(output_path)

        logger.info("Output saved to {}".format(config.OUTPUT_PATH))

if __name__ == '__main__':
    fire.Fire(CreateInstances)
