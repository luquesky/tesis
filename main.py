#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file> <feature>
  main.py hybrid_tama <path_to_wav_file> <feature>
  main.py extract_features <path_to_wav_file> <start> <end>
"""
from docopt import docopt
from sympy import Interval
from speech import tama, hybrid_tama, SpeechBuilder

def run_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    print tama(speech, feature)

def run_hybrid_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    print hybrid_tama(speech, feature)

def extract_features(arguments):
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    interval = Interval(float(arguments["<start>"]), float(arguments["<end>"]))
    print speech.get_features(interval)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')

    if arguments["tama"]:
        run_tama(arguments)
    elif arguments["hybrid_tama"]:
        run_hybrid_tama(arguments)
    elif arguments["extract_features"]:
        extract_features(arguments)

