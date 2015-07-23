#! coding: utf-8
import config
import pandas as pd
from tama import tama, normalize
from tsa import entrainment, autoregressive_prewhitening

class TaskTooShort(Exception):
    pass

class Analyzer(object):

    def __init__(self, feature):
        self.feature = feature

    def analyze(self, sessions):
        session_table = pd.DataFrame(columns=self.__columns__())

        for session in sessions:
            for task in session.tasks:
                try:
                    entry_name = "S%s-T%s" % (session.number, task.number)
                    session_table.loc[entry_name+"-A"], session_table.loc[entry_name+"-B"] = self.__analyze_task(session, task)
                except TaskTooShort as e:
                    continue
        return session_table

    def __generate_task_series(self, A, B, meanA, meanB, session, task):
        l_AB, E_AB, l_BA, E_BA = entrainment(A, B, lags=range(-6, 6))

        AB_data = pd.Series({
            "session": session.number,
            "task": task.number,
            "speaker": "A",
            "count": A.count(),
            "entrainment" : E_AB,
            "best_lag" : abs(l_AB),
            "tama_mean": meanA,
        })

        BA_data = pd.Series({
            "session": session.number,
            "task": task.number,
            "speaker": "B",
            "count": B.count(),
            "entrainment" : E_BA,
            "best_lag" : abs(l_BA),
            "tama_mean": meanB,
        })

        return AB_data, BA_data

    def __analyze_task(self, session, task):
        task_data = pd.Series()

        A, meanA = tama(task.speechA, self.feature)
        B, meanB = tama(task.speechB, self.feature)

        if (A.count() < config.SERIES_LENGTH_THRESHOLD) or (B.count() < config.SERIES_LENGTH_THRESHOLD):
            raise TaskTooShort("Series too short")

        nA = normalize(A, meanA)
        nB = normalize(B, meanB)

        rA, rB = autoregressive_prewhitening(nA, nB)
        task_key = task.name.replace("Task", "T").replace(" ", "")

        return self.__generate_task_series(rA, rB, meanA=meanA, meanB=meanB, session=session, task=task)

    def __columns__(self):
        return ["task",
            "session",
            "count",
            "speaker",
            "tama_mean",
            "entrainment",
            "best_lag" ]