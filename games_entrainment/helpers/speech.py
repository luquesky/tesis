from ..speech import Speech
from sympy import Interval
from ..speech import (
    StandardAcousticsExtractor,
    VoiceAnalysisExtractor,
    CompositeExtractor,
    CachedExtractor
)


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
