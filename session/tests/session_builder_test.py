#! coding:utf-8
from unittest import TestCase
from .. import SessionBuilder

class SessionBuilderTest(TestCase):
    def test_it_builds_it_with_both_speechs(self):
        builder = SessionBuilder("data/test/session.tasks")

        session = builder.session

        self.assertAlmostEqual(session.speechA.length(), 122.98)
        self.assertAlmostEqual(session.speechB.length(), 122.98)
