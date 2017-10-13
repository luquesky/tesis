#! coding:utf-8
"""Script extractor of acoustic features."""
import os
from distutils.spawn import find_executable
import logging
import subprocess
from games_entrainment import config

logger = logging.getLogger('main')


class ScriptExtractor(object):
    """
    An object of this class has the responsibility of extracting the features
    (f_0, ) out of a wav file.

    It should be created with both a path to the wav file, and to a praat
    script which returns the features (in the project, they are at scripts/)
    """

    def __init__(
        self,
        path_to_script,
        path_to_praat,
        path_to_wav,
        min_pitch=75,
        max_pitch=500
    ):
        """
        Constructor.

        Parameters:
        ----------

        path_to_script: string
            Path to praat script

        path_to_wav: string
            Path of the wav to extract features

        path_to_praat: string
            Path to the praat binary

        min_pitch: numeric
            Min pitch of the pass-band filter

        max_pitch: numeric
            Max pitch of the pass-band filter
        """
        self.path_to_script = path_to_script
        self.path_to_praat = path_to_praat
        self.path_to_wav = path_to_wav
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch

    def extract_features(self, interval):
        """Extract features from the given interval."""
        try:
            command = self.__get_command_to_execute(interval)

            output = subprocess.check_output(command)
            features = self.__convert_to_dict(output)

            return features
        except:
            logger.error(
                "There was an error calling %s with interval %s" %
                (self.path_to_script, interval))
            return {}

    def __convert_to_dict(self, command_output):
        ret = [line.split(':') for line in command_output.splitlines()]

        return {k.upper(): self.__convert_to_float(v) for (k, v) in ret}

    def __convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return float('nan')

    # FIXME: Change min & max pitch
    def __get_command_to_execute(self, interval):
        return (self.path_to_praat, self.path_to_script,
                self.path_to_wav, str(interval.inf), str(interval.sup),
                str(self.min_pitch), str(self.max_pitch))


def StandardAcousticsExtractor(path_to_wav, gender):
    """Extractor using extractStandardAcoustics.praat."""
    path_to_script = os.path.join(
        config.PRAAT_SCRIPTS_PATH,
        "extractStandardAcoustics.praat")

    if gender == 'm':
        min_pitch, max_pitch = 50, 300
    elif gender == 'f':
        min_pitch, max_pitch = 75, 500
    else:
        raise ValueError("{} is not a valid gender".format(gender))

    return ScriptExtractor(
        path_to_script=path_to_script,
        path_to_praat=find_executable("praat"),
        path_to_wav=path_to_wav,
        min_pitch=min_pitch,
        max_pitch=max_pitch,
    )


def VoiceAnalysisExtractor(path_to_wav, gender):
    """Extractor using voice-analysis.praat."""
    path_to_script = os.path.join(
        config.PRAAT_SCRIPTS_PATH,
        "voice-analysis.praat"
    )

    return ScriptExtractor(
        path_to_script=path_to_script,
        path_to_praat=find_executable("praat"),
        path_to_wav=path_to_wav
    )
