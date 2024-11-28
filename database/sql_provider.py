import os
from string import Template


class SQLProvider:

    def __init__(self, file_path):
        self.scripts = {}
        for file in os.listdir(file_path):
            _sql = open(f'{file_path}/{file}').read()
            self.scripts[file] = Template(_sql)

    def get(self, file, **kwargs):
        sql = self.scripts[file].substitute(**kwargs)
        return sql
