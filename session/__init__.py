#! coding:utf-8
from session import Session
from session_builder import SessionBuilder
from session_mapper import SessionMapper
from social_variables_builder import SocialVariablesBuilder
from task import Task


def load_session(session_number):
    mapper = SessionMapper()
    num = str(session_number).zfill(2)
    name = "session-%s" % num
    tasks_path = "data/games-corpus/session_%s/s%s.objects.1.tasks" % (num, num)
    return mapper.fetch(tasks_path, name=name)
