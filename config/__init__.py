#! coding:utf-8
import logging
import os

# Perhaps this could be improved...
def project_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, os.path.pardir))


def init_logging():
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(LOG_DIR, 'main.log'))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    logger.addHandler(fh)
    logger.addHandler(ch)


ROOT_DIR = project_dir()
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOG_DIR = os.path.join(ROOT_DIR, "log")

TASK_LENGTH_THRESHOLD = 40

SERIES_FRAME_STEP = 8
SERIES_FRAME_LENGTH = 16

SERIES_LENGTH_THRESHOLD = 5
CORRELATION_LENGTH_THRESHOLD = 4

init_logging()
