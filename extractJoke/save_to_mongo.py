#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

db_info = {"ip":"localhost", "port":27017, "db_name":"qiushi_data", "collection":"first_get"}

class SaveToMongo(object):
    def __init__(self):
        self._db_conn = None
        self._db = None
        self.open_db()

    def open_db(self):
        self._db_conn = pymongo.MongoClient(db_info['ip'], db_info['port'])
        self._db = self._db_conn[db_info['db_name']]

    def save_data(self, data):
        self._db[db_info['collection']].insert(data)

    def clear_data(self):
        self._db[db_info['collection']].remove()
