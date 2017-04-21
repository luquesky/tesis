#! coding: utf-8
import os
import logging
import dill
import pickle
from . import SessionBuilder

logger = logging.getLogger('main')


class SessionMapper(object):
    def __init__(self, session_info):
        self.session_info = session_info

    def fetch(self, path_to_tasks, number, **opts):
        try:
            with open(self.__pickle_file_path(path_to_tasks), "rb") as h:
                return pickle.load(h)
        except:
            # At any exception => build it from scratch
            logger.info("Pickle for session %s not found. Building from scratch" % path_to_tasks)
            info = self.session_info.loc[number]
            opts.update(info.to_dict())

            return SessionBuilder(path_to_tasks, number, **opts).session

    def save(self, session):
        with open(self.__pickle_file_path(session.path_to_tasks), "wb") as h:
            return pickle.dump(session, h)

    def __pickle_file_path(self, path_to_tasks):
        abs_path = os.path.abspath(path_to_tasks)
        filename, extension = os.path.splitext(abs_path)
        return "%s.session.pickle" % (filename)
