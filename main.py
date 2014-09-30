#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file> <feature>
  main.py hybrid_tama <path_to_wav_file> <feature>
  main.py compare <feature> <path_to_wav1> <path_to_wav2>
  main.py extract_features <path_to_wav_file> <start> <end>

"""
import config
import matplotlib.pyplot as plt
from docopt import docopt
from sympy import Interval
from commands import plot_tama, plot_tamas
from speech import tama, hybrid_tama, SpeechBuilder

def run_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    plot_tama(speech, feature, hybrid=False)

def run_hybrid_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    plot_tama(speech, feature)


def extract_features(arguments):
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    interval = Interval(float(arguments["<start>"]), float(arguments["<end>"]))
    print speech.get_features(interval)

def compare(arguments):
    feature = arguments["<feature>"]
    speech1 = SpeechBuilder(arguments["<path_to_wav1>"]).speech
    speech2 = SpeechBuilder(arguments["<path_to_wav2>"]).speech
    plot_tamas(speech1, speech2, feature)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')

    if arguments["tama"]:
        run_tama(arguments)
    elif arguments["hybrid_tama"]:
        run_hybrid_tama(arguments)
    elif arguments["extract_features"]:
        extract_features(arguments)
    elif arguments["compare"]:
        compare(arguments)

