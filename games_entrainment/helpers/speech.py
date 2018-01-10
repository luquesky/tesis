#! coding: utf-8
import csv
from ..speech import Speech, WordInterval
from .. import config
from sympy import Interval
from pydub import AudioSegment
from ..speech import (
    StandardAcousticsExtractor,
    VoiceAnalysisExtractor,
    CompositeExtractor,
    CachedExtractor
)
from ..tama import normalized_tama


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


def get_ctm_word_intervals(path_to_words,chan=''):
    """Get word intervals for a task from a csv or similar

    Parameters:
    ----------

    path_to_words: String
        Path to ctm file
    """
    return get_word_intervals(
        path_to_words,
        create_interval_function=create_ctm_interval,chan=chan
    )



def get_word_intervals(path_to_words, task_interval=None,
                       create_interval_function=create_games_corpus_interval, chan=''):
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
        #dialect = csv.Sniffer().sniff(test_words.read(1024))
        dialect = csv.Sniffer().sniff(test_words.readline())
        test_words.seek(0)
        rows = csv.reader(test_words, dialect)

        for row in rows:
            if chan != '':
                if row[0].count(chan) > 0:
                    #print (row)
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
            else:
                #print (row)
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
                  time_start=None, time_end=None, chan=''):
    """Create Speech object out of a CSV Row.

    Parameters
    ----------
    wav_path: String
        Absolute or relative path to wav
    gender: 'm' or 'f'
        Male or Female
    time_start, time_end: float
        Time interval to consider from the wav.
        If None, considers the whole wav.
    word_intervals: List of tuples (word, simpy.Interval)
        Example:

    """

    extractor = build_extractor(wav_path, gender)
    time_start = time_start or 0
    time_end = time_end or AudioSegment.from_wav(wav_path).duration_seconds

    interval = Interval(time_start, time_end)

    return Speech(
        path_to_wav=wav_path,
        interval=interval,
        word_intervals=word_intervals,
        gender=gender.lower(),
        feature_extractor=extractor,
    )


class TaskTooShort(Exception):
    u"""Exception for short task."""

    pass


def create_tama(speech, feature):
    """Create tama for speech and feature."""
    A = normalized_tama(speech, feature)

    if (A.count() < config.SERIES_LENGTH_THRESHOLD):
        #raise TaskTooShort("Series too short")
        print('Series too short')
    return A
