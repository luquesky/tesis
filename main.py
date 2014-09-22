#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file> <feature>
  main.py hybrid_tama <path_to_wav_file> <feature>
"""
from docopt import docopt
from speech import tama, hybrid_tama, SpeechBuilder

def run_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    print tama(speech, feature)

def run_hybrid_tama(arguments):
    feature = arguments["<feature>"]
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    print tama(speech, feature)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')

    if arguments["tama"]:
        run_tama(arguments)
    if arguments["hybrid_tama"]:
        run_hybrid_tama(arguments)
