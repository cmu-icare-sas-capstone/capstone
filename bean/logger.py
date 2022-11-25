from logging import Logger
from logging import StreamHandler
from sys import stdout

logger = Logger("log", "DEBUG")
handler = StreamHandler(stdout)
logger.addHandler(handler)
