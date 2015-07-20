#! coding:utf-8
from unittest import TestCase
from .. import SocialVariablesBuilder, SessionBuilder


class SocialVariablesBuilderTest(TestCase):
    def test_it_sets_empty_variables_if_just_headers_given(self):
        session = SessionBuilder("data/test/session.tasks", number=1).session
        builder = SocialVariablesBuilder([session])

        builder.build(iter([["hitid"]]))

        self.assertEqual(session.tasks[0].social_variables, {})

    def test_it_sets_a_variable(self):
        session = SessionBuilder("data/test/session.tasks", number=1).session
        builder = SocialVariablesBuilder([session])

        builder.build(iter([['hitid', "foo"], ["g1t1", 5]]))

        self.assertEqual(session.tasks[0].social_variables, {"foo": 5})
