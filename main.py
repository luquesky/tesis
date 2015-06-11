#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file> <feature>
  main.py hybrid_tama <path_to_wav_file> <feature>
  main.py save_images <path_to_task_file>
  main.py compare <feature> <path_to_wav1> <path_to_wav2>
  main.py extract_features <path_to_wav_file> <start> <end>
"""
from docopt import docopt
from sympy import Interval
from speech import SpeechBuilder


def extract_features(arguments):
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    interval = Interval(float(arguments["<start>"]), float(arguments["<end>"]))
    print speech.get_features(interval)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')

    if arguments["extract_features"]:
        extract_features(arguments)
