from sympy import Interval
from speech import SpeechBuilder
"""
This should be replaced with FactoryBoy or something of the kind
"""
def build_speech(**opts):
    defaults = {
        'path_to_file': 'tama/tests/data/test.wav',
        'interval': Interval(0, 30),
        'gender': 'm',
        'speaker_id': 101
    }

    defaults.update(opts)

    return SpeechBuilder(**defaults).speech