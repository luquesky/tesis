#! coding: utf-8
from ..speech import Speech, WordInterval
from sympy import Interval
import csv
from ..speech import (
    StandardAcousticsExtractor,
    VoiceAnalysisExtractor,
    CompositeExtractor,
    CachedExtractor
)


def create_games_corpus_interval(row):
    start = float(row[0])
    end = float(row[1])
    transcription = row[2]

    return WordInterval(start, end, transcription)


def create_ctm_interval(row):
    start = float(row[1])
    length = float(row[2])
    transcription = row[3]

    return WordInterval(start, start+length, transcription)


def get_ctm_word_intervals(path_to_words):
    """Get word intervals for a task from a csv or similar

    Parameters:
    ----------

    path_to_words: String
        Path to ctm file
    """
    return get_word_intervals(
        path_to_words,
        create_interval_function=create_ctm_interval,
    )



def get_word_intervals(path_to_words, task_interval=None,
                       create_interval_function=create_games_corpus_interval):
    """Get word intervals for a task from a csv or similar

    Parameters:
    ----------

    path_to_words: String
        Path to transcription file

    task_interval: sympy.Interval
        Interval of time to consider.
        Words will only be drawn inside this time interval.
        If None, will get all the words.

    Optional Parameters
    -------------------

    create_games_corpus_interval: function
        Function receiving a CSV row
    """
    word_intervals = []

    with open(path_to_words) as test_words:
        # Get dialect
        dialect = csv.Sniffer().sniff(test_words.read(1024))
        test_words.seek(0)
        rows = csv.reader(test_words, dialect)

        for row in rows:
            """Search for intervals in current task."""
            wint = create_interval_function(row)

            if task_interval:
                if wint.inf > task_interval.sup:
                    break

                intersection = task_interval.intersect(wint.interval)
                if intersection.measure > 0:
                    word_intervals.append(wint)
            else:
                word_intervals.append(wint)

    return word_intervals


def build_extractor(wav_path, gender):
    """Build acoustic extractor for given speech."""
    extractor1 = StandardAcousticsExtractor(wav_path, gender)
    extractor2 = VoiceAnalysisExtractor(wav_path, gender)

    return CachedExtractor(CompositeExtractor(extractor1, extractor2))


def create_speech(wav_path, gender, word_intervals,
                  time_start=None, time_end=None):
    """Create Speech object out of a CSV Row.

    Parameters
    ----------
    wav_path: String
        Absolute or relative path to wav
    gender: 'M' or 'F'
        Male or Female
    time_start, time_end: float
        Time interval to consider from the wav.
        If None, considers the whole wav.
    word_intervals: List of tuples (word, simpy.Interval)
        Example:

    """
    extractor = build_extractor(wav_path, gender)
    interval = Interval(time_start, time_end)

    return Speech(
        path_to_wav=wav_path,
        interval=interval,
        word_intervals=word_intervals,
        gender=gender,
        feature_extractor=extractor,
    )
