#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from speech import tama, SpeechBuilder

def run_tama(arguments):
    speech = SpeechBuilder(arguments["<path_to_wav_file>"]).speech
    print tama(speech, "F0_MEAN")

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Tesis 0.0.1')

    if arguments["tama"]:
        run_tama(arguments)
