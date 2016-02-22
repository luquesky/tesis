#! coding:utf-8
import os
from session import Session
from session_builder import SessionBuilder
from session_mapper import SessionMapper
from social_variables_builder import SocialVariablesBuilder
from task import Task


def task_directory(num):
  current_dir = os.path.dirname(__file__)
  parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))

  return os.path.join(parent_dir, "data/games-corpus/session_%s/s%s.objects.1.tasks" % (num, num))


def load_session(session_number):
    mapper = SessionMapper()
    num = str(session_number).zfill(2)
    name = "session-%s" % num

    return mapper.fetch(task_directory(num), name=name, number=session_number)
