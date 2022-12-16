import logging
from sys import stdout


def get_logger(name):
    logger = logging.Logger(name)
    logger.setLevel(level=logging.ERROR)
    handler = logging.StreamHandler(stdout)
    logger.addHandler(handler)
    return logger

