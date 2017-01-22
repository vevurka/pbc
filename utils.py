# -*- coding: utf-8 -*-

from contextlib import contextmanager
import os
import sqlite3


@contextmanager
def db_connection():
    try:
        connection = sqlite3.connect('config/database.db',
                                     detect_types=sqlite3.PARSE_DECLTYPES)
        yield connection.cursor()

    finally:
        connection.commit()
        connection.close()


def cleanup(config):

    def del_files(directory):
        [os.remove(os.path.join(directory, f)) for f in os.listdir(directory)]

    try:
        os.remove(config['files']['zipfile'])
        del_files(config['files']['zipdir'])
        del_files(config['files']['imagesdir'])
    except Exception as e:
        print(e)