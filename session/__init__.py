#! coding:utf-8
"""Entry point for session module."""
import os
import csv
import config
import pandas as pd
from session import Session
from session_builder import SessionBuilder
from session_mapper import SessionMapper
from social_variables_builder import SocialVariablesBuilder
from task import Task


def task_directory(num):
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))

    return os.path.join(parent_dir, "data/games-corpus/session_%s/s%s.objects.1.tasks" % (num, num))


def load_session_info():
    """Load default session info"""
    l = list(csv.reader(open(config.SESSION_INFO_PATH)))

    headers, data = l[0], l[1:]

    df = pd.DataFrame(data, columns=headers)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.set_index("session")

    return df


def load_session(session_number):
    mapper = SessionMapper(load_session_info())
    num = str(session_number).zfill(2)
    name = "session-%s" % num

    return mapper.fetch(task_directory(num), name=name, number=session_number)
