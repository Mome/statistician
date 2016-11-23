from collections import namedtuple
import os
import json
from datetime import datetime

Record = namedtuple('Record', [
    'name',
    'start_ts',
    'select_ts',
    'comp_ts',
    'perf'])

class Protocol:
    def __init__(self, name):
        self.name = name
        self.records = {}

    def save(self, name=None):
        if not name:
            name = self.name
        fullpath = os.path.join(path, name)
        with open(fullpath) as f:
            json.dump(self.records)

    def record(self, name, start_ts, selection_ts, computation_ts, performance):
        rec = Record(name, start_ts, selection_ts, computation_ts, performance)
        self.add(rec)
        return rec

    def add(self, rec):
        if name not in self.records:
            self.records[name] = []
        self.records[name].append(rec)

    def get_best(self):
        return max(
            self.records.items(),
            key = lambda item : item.perf)
