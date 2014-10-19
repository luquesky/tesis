#! coding:utf-8
import os
from . import Session
from speech import SpeechBuilder

class SessionBuilder(object):
    def __init__(self, path_to_tasks):
        self.path_to_tasks = os.path.abspath(path_to_tasks)

    @property
    def session(self):
        speechA, speechB = self.__build_speechs()

        return Session([], speechA, speechB)

    def __build_speechs(self):
        filename, extension = os.path.splitext(self.path_to_tasks)

        path_to_A = "%s.A.wav" % filename
        path_to_B = "%s.A.wav" % filename

        return SpeechBuilder(path_to_A).speech, SpeechBuilder(path_to_B).speech

