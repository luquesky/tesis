#! coding: utf-8
import os
import pickle
from . import SpeechBuilder

class SpeechMapper(object):
    def __init__(self):
        pass

    def fetch(self, speech_path):
        try:
            with open(self.__pickle_file_path(speech_path), "rb") as h:
                return pickle.load(h)
        except:
            # At any exception => build it from scratch
            return SpeechBuilder(speech_path).speech

    def save(self, speech):
        with open(self.__pickle_file_path(speech.path_to_wav), "wb") as h:
            return pickle.dump(speech, h)


    def __pickle_file_path(self, speech_path):
        abs_path = os.path.abspath(speech_path)
        filename, extension = os.path.splitext(abs_path)
        return "%s.pickle" % (filename)
