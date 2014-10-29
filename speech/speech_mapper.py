#! coding: utf-8
import os
import pickle

class SpeechMapper(object):
    def __init__(self):
        pass

    def fetch(self, speech_path):
        with open(self.__pickle_file_path(speech_path), "rb") as h:
            return pickle.load(h)

    def __pickle_file_path(self, speech_path):
        abs_path = os.path.abspath(speech_path)
        filename, extension = os.path.splitext(abs_path)
        return "%s.pickle" % (filename)
