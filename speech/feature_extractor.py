#! coding:utf-8
# An object of this class has the responsibility of extracting the features (f_0, ) out of a wav file
# It should be created with both a path to the wav file, and to a praat script which returns the features (in the project, they are at scripts/)
import logging
import subprocess

logger = logging.getLogger('main')

class FeatureExtractor(object):

    # All paths should be absolute...praat
    def __init__(self, path_to_script, path_to_praat, path_to_wav):
        self.path_to_script = path_to_script
        self.path_to_praat = path_to_praat
        self.path_to_wav = path_to_wav
        self.cached_features = {}

    def extract_features(self, interval):
        if self.cached_features.has_key(interval):
            logger.debug("Using cached value for %s" % interval)
            return self.cached_features[interval]

        command = self.__get_command_to_execute(interval)
        logger.debug("Command to invoke feature extractor:")
        logger.debug(command)

        output = subprocess.check_output(command)
        features = self.__convert_to_dict(output)
        self.cached_features[interval] = features

        return features

    def __convert_to_dict(self, command_output):
        ret = [line.split(':') for line in command_output.splitlines()]

        return dict([(k, self.__convert_to_float(v)) for (k,v) in ret])

    def __convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return float('nan')

    # FIXME: Change min & max pitch
    def __get_command_to_execute(self, interval):
        return (self.path_to_praat, self.path_to_script, self.path_to_wav, str(interval.inf), str(interval.sup), "75", "500")
