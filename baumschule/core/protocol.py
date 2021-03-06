from collections import namedtuple
import os
import json
from datetime import datetime
from itertools import chain

from .utils import get_minium_perfs


class Protocol:
    def write(self, *args, **kwargs):
        raise NotImplementedError()

    def get_min(self):
        raise NotImplementedError()

    def get_max(self):
        raise NotImplementedError()


class SimpleProtocol(Protocol, list):
    def write(self, instance, perf, **kwargs):
        self.append((instance, perf))

    def get_min(self):
        return get_best(self, min)

    def get_max(self):
        return get_best(self, max)

    def get_best(self, opt_func):
        """
        Returns all entrys having the best performance.

        """
        filt = lambda rec : rec.perf
        perfs = map(filt, self)
        best_perf = opt_func(perf)
        filt = lambda rec : rec.perf == best_perf
        return tuple(filter(filt, self))


class PerfDictProtocol(Protocol, dict):
    def write(self, instance_str, instance, perf, **kwargs):
        self[instance_str] = (instance, perf)


varnames = 'name start_ts select_time comp_time perf'.split()
Record = namedtuple('Record', varnames)

class StandardProtocol(Protocol, list):
    def write(self, instance_str, start_ts, select_time, comp_time, perf, **kwargs):
        record = Record(instance_str, start_ts, select_time, comp_time, perf)
        self.append(record)

    def to_dataframe(self):
        import pandas as pd
        df = pd.DataFrame.from_records(
            data = list(self),
            columns = self[0]._fields,
        )
        return df

    def to_csv(self, filename):
        df = self.to_dataframe()
        df.to_csv(filename)

    def get_min(self):
        best = self[0]
        for record in self[1:]:
            if record.perf < best.perf:
                best = record
        return best

    def minium_perfs(self):
        return get_minium_perfs(self)
