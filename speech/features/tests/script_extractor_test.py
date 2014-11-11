#! coding:utf-8
from mock import patch
from unittest import TestCase
from sympy import Interval

from .. import ScriptExtractor

class ScriptExtractorTest(TestCase):
    @patch('speech.features.script_extractor.subprocess')
    def test_feature_extractor_calls_script(self, subprocess_mock):
        extractor = ScriptExtractor(
            path_to_praat="/bin/praat",
            path_to_script="foo.praat",
            path_to_wav="test.wav")

        extractor.extract_features(Interval(0, 10))

        subprocess_mock.check_output.assert_called_with(("/bin/praat", "foo.praat", "test.wav", "0", "10", "75", "500"))

    @patch('speech.features.script_extractor.subprocess')
    def test_feature_extractor_converts_to_dict(self, subprocess_mock):
        subprocess_mock.check_output.return_value = 'SECONDS:5.000\nF0_MAX:506.305\nF0_MIN:279.057\n'
        extractor = ScriptExtractor(
            path_to_praat="/bin/praat",
            path_to_script="foo.praat",
            path_to_wav="test.wav")

        ret = extractor.extract_features(Interval(0, 10))
        self.assertItemsEqual(ret.keys(), ["SECONDS", "F0_MAX", "F0_MIN"])
