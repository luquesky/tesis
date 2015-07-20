#! coding: utf-8
import re


class SocialVariablesBuilder(object):
    def __init__(self, sessions):
        self.sessions = sessions

    # variables should be an iterable (generated with csv.rows)
    def build(self, variables):
        for session in self.sessions:
            for task in session.tasks:
                task.social_variables = {}

        header = variables.next()

        for row in variables:
            sv_hash = dict(zip(header, row))

            task = self.__find_task__(sv_hash.pop("hitid"))

            task.social_variables = sv_hash

    def __find_task__(self, task_id):
        s = re.match(r"g(?P<SESSION>[0-9]+)t(?P<TASK>[0-9]+)", task_id)
        session_number = int(s.groupdict()["SESSION"])
        task_number = int(s.groupdict()["TASK"])

        session = next(s for s in self.sessions if s.number == session_number)

        task = next(t for t in session.tasks if t.number == task_number)

        return task
