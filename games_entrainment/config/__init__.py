#! coding:utf-8
import logging
import os

# Perhaps this could be improved...
def project_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir,
                                        os.path.pardir,
                                        os.path.pardir))


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
CORPUS_DIR = os.path.join(DATA_DIR, "games-corpus")
LOG_DIR = os.path.join(ROOT_DIR, "log")
TABLES_DIR = os.path.join(ROOT_DIR, "tables")

PRAAT_SCRIPTS_PATH = os.path.join(ROOT_DIR, "praat_scripts")

SESSION_INFO_PATH = os.path.join(CORPUS_DIR, "session-info.csv")


OUTPUT_PATH = os.path.join(TABLES_DIR, "output.csv")

TASK_LENGTH_THRESHOLD = 40
SERIES_FRAME_STEP = 8
SERIES_FRAME_LENGTH = 16

SERIES_LENGTH_THRESHOLD = 5
CORRELATION_LENGTH_THRESHOLD = 4

FEATURES = [
    "F0_MEAN",
    "F0_MAX",
    "ENG_MAX",
    "ENG_MEAN",
    'NOISE_TO_HARMONICS_RATIO',
    'SOUND_ALL_LOCAL_JITTER',
    'SOUND_ALL_LOCAL_SHIMMER',
    'SOUND_VOICED_LOCAL_JITTER',
    'SOUND_VOICED_LOCAL_SHIMMER'
]

init_logging()
