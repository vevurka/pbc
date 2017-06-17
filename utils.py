# -*- coding: utf-8 -*-

from contextlib import contextmanager
import logging
import logging.config
import os
import sqlite3


logger = logging.getLogger()


LOGGER_CONFIG = {
    'version': 1,
    'formatters': {
        'main': {
            'format': '%(asctime)-15s %(message)s',
            }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'pankreator_app.log',
            'formatter': 'main'
        }
        },
    'root': {
        'handlers': ['file', ],
        'level': 'INFO',
        'propagate': 'yes'
    }
}


def initialize_logging():
    logging.config.dictConfig(LOGGER_CONFIG)


@contextmanager
def db_connection(db_path):
    try:
        connection = sqlite3.connect(db_path,
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
        logger.error(e)


class APIException(Exception):

    pass


class ConverterException(Exception):

    pass