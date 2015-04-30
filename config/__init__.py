#! coding:utf-8
import logging


def init_logging():
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('log/main.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    logger.addHandler(fh)
    logger.addHandler(ch)


TASK_LENGTH_THRESHOLD = 100

init_logging()
