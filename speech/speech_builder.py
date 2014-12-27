#! coding: utf-8
import os
import csv
from distutils.spawn import find_executable
from word_interval import WordInterval
from features import ScriptExtractor, CachedExtractor, CompositeExtractor, SyllabeExtractor, PhonemeExtractor
from speech import Speech

DATA_DIR = "speech/tests/integration/data"

class SpeechBuilder(object):
    def __init__(self, path_to_file):
        self.path_to_wav = os.path.abspath(path_to_file)
        filename, extension = os.path.splitext(self.path_to_wav)
        self.path_to_words = "%s.words" % filename

    def get_word_intervals(self):
        if hasattr(self, "intervals"):
            return self.intervals

        self.intervals = []
        with open(self.path_to_words) as test_words:
            rows = csv.reader(test_words, delimiter=" ")
            for row in rows:
                self.intervals.append(WordInterval(float(row[0]), float(row[1]),row[2]))
        return self.intervals

    # This is quite ad hoc
    def build_feature_extractor(self):
        extractor1 = ScriptExtractor(
            path_to_script = os.path.abspath("scripts/extractStandardAcoustics.praat"),
            path_to_praat = find_executable("praat"),
            path_to_wav=self.path_to_wav
        )

        extractor2 = ScriptExtractor(
            path_to_script = os.path.abspath("scripts/voice-analysis.praat"),
            path_to_praat = find_executable("praat"),
            path_to_wav=self.path_to_wav
        )


        syllabe_extractor = self.build_syllabe_extractor()
        phoneme_extractor = self.build_phoneme_extractor()

        return CachedExtractor(CompositeExtractor(
                extractor1,
                extractor2,
                syllabe_extractor,
                phoneme_extractor
            )
        )

    @property
    def speech(self):
        word_intervals = self.get_word_intervals()
        feature_extractor = self.build_feature_extractor()
        return Speech(
            path_to_wav=self.path_to_wav,
            word_intervals=word_intervals,
            feature_extractor=feature_extractor)


    def build_syllabe_extractor(self):
        with open("data/sylcounts.txt") as f:
            rows = csv.reader(f, delimiter='\t')
            syllabe_count = {k.lower():int(v) for k,v in rows}
            return SyllabeExtractor(
                word_intervals= self.get_word_intervals(),
                syllabe_count=syllabe_count
            )

    def build_phoneme_extractor(self):
        with open("data/phonetic-dictionary-games.txt") as f:
            rows = csv.reader(f, delimiter=" ")
            mapping = {'#': 0}

            for row in rows:
                key = row[0].lower()
                value = len(row) - 1
                if key in mapping:
                    mapping[key] = max(mapping[key], value)
                else:
                    mapping[key] = value

            return PhonemeExtractor(self.get_word_intervals(), mapping)

