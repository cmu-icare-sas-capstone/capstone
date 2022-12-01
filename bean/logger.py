import logging
from sys import stdout


def get_logger(name):
    logger = logging.Logger(name)
    handler = logging.StreamHandler(stdout)
    logger.addHandler(handler)
    return logger

