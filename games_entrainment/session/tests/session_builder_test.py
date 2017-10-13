#! coding:utf-8
import pandas as pd
from unittest import TestCase
from .. import SessionBuilder


class SessionBuilderTest(TestCase):
    def test_it_builds_with_tasks(self):
        builder = SessionBuilder(
            "data/test/session.tasks",
            number=1, idA=1, idB=2, genderA='m', genderB='m'
        )

        session = builder.session

        self.assertEqual(len(session.tasks), 1)

    def test_it_builds_with_number(self):
        builder = SessionBuilder(
            "data/test/session.tasks",
            number=3, idA=1, idB=2, genderA='m', genderB='m'
        )

        session = builder.session

        self.assertEqual(session.number, 3)
