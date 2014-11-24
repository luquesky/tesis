#! coding:utf-8
"""Main program

Usage:
  main.py tama <path_to_wav_file> <feature>
  main.py hybrid_tama <path_to_wav_file> <feature>
  main.py save_images <path_to_task_file>
  main.py compare <feature> <path_to_wav1> <path_to_wav2>
  main.py extract_features <path_to_wav_file> <start> <end>
"""
import os
import config
import matplotlib.pyplot as plt
from docopt import docopt
from sympy import Interval
from session import SessionBuilder
from commands import plot_tama, plot_tamas
from speech import SpeechBuilder

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

def save_images(arguments):
    filename = arguments["<path_to_task_file>"]
    dirname = os.path.dirname(filename)

    session = SessionBuilder(filename).session
    features = ['VCD2TOT_FRAMES', 'F0_MEAN', 'F0_MAX', 'ENG_MAX', 'ENG_MEAN', "NOISE_TO_HARMONICS_RATIO", "SOUND_ALL_LOCAL_JITTER", "SOUND_ALL_LOCAL_SHIMMER", "SOUND_VOICED_LOCAL_JITTER", "SOUND_VOICED_LOCAL_SHIMMER"]

    analysis = session.analyze(features)

    for index, task in enumerate(session.tasks):
        for feature in features:
            try:
                os.mkdir(os.path.join(dirname, feature))
            except OSError:
                pass

            TA, averagesA = analysis[task][feature]["A"]
            TB, averagesB = analysis[task][feature]["B"]

            plt.plot(TA, averagesA)
            plt.plot(TB, averagesB)

            plt.xlabel("Time")
            plt.ylabel("Average %s" % feature)

            image_file = os.path.join(dirname, feature, "task.%02d.jpg" % (index+1))
            plt.savefig(image_file)
            plt.close()



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
    elif arguments["save_images"]:
        save_images(arguments)

