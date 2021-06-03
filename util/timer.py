import time

from app.util.logger import log

DEFAULT_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"


def format_time(timestamp, fmt=DEFAULT_TIME_FORMAT):
    return time.strftime(fmt, time.localtime(timestamp))


class Timer(object):
    def __init__(self):
        self._start = 0
        self._is_start = False
        pass

    def start(self):
        self._is_start = True
        self._start = time.time()

    def reset(self):
        self._start = time.time()

    def duration(self, note=''):
        now = time.time()
        elapsed_time = now - self._start
        log.info("[ Timer<%s> %s] from %s to %s , elapsed time %.3fs", id(self), note,
                 format_time(self._start), format_time(now), elapsed_time)
        return elapsed_time
