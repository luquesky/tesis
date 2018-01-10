#! coding: utf-8
import os
import csv
from games_entrainment import config
from distutils.spawn import find_executable
from .word_interval import WordInterval
from .features import StandardAcousticsExtractor, VoiceAnalysisExtractor, CachedExtractor, CompositeExtractor, SyllabeExtractor, PhonemeExtractor
from .speech import Speech


class SpeechBuilder(object):
    def __init__(self, path_to_file, interval, speaker_id, gender, feature_extractor=None):
        self.path_to_wav = os.path.abspath(path_to_file)
        self.interval = interval
        self.feature_extractor = feature_extractor
        self.speaker_id = speaker_id
        self.gender = gender

        filename, extension = os.path.splitext(self.path_to_wav)
        self.path_to_words = "%s.words" % filename

    def get_word_intervals(self):
        if hasattr(self, "word_intervals"):
            return self.word_intervals

        self.word_intervals = []
        with open(self.path_to_words) as test_words:
            rows = csv.reader(test_words, delimiter=" ")
            for row in rows:
                wint = WordInterval(float(row[0]), float(row[1]),row[2])
                if wint.inf > self.interval.sup:
                    break

                intersection = self.interval.intersect(wint.interval)
                if intersection.measure > 0:
                    self.word_intervals.append(wint)

        return self.word_intervals

    # This is quite ad hoc
    def build_feature_extractor(self):
        extractor1 = StandardAcousticsExtractor(self.path_to_wav, self.gender)
        extractor2 = VoiceAnalysisExtractor(self.path_to_wav, self.gender)

        syllabe_extractor = self.build_syllabe_extractor()
        phoneme_extractor = self.build_phoneme_extractor()

        composed_extractor = CompositeExtractor(extractor1, extractor2, syllabe_extractor, phoneme_extractor)
        return CachedExtractor(composed_extractor)

    @property
    def speech(self):
        feature_extractor = self.feature_extractor or self.build_feature_extractor()
        return Speech(
            path_to_wav=self.path_to_wav,
            interval=self.interval,
            word_intervals=self.word_intervals,
            gender=self.gender,
            feature_extractor=feature_extractor)


    def build_syllabe_extractor(self):
        syllabes_path = os.path.join(config.DATA_DIR, "sylcounts.txt")

        with open(syllabes_path) as f:
            rows = csv.reader(f, delimiter='\t')
            syllabe_count = {k.lower():int(v) for k,v in rows}
            return SyllabeExtractor(
                word_intervals= self.get_word_intervals(),
                syllabe_count=syllabe_count
            )

    def build_phoneme_extractor(self):
        phonetic_dict_path = os.path.join(config.DATA_DIR, "phonetic-dictionary-games.txt")
        with open(phonetic_dict_path) as f:
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
