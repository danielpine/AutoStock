import util
import logging
import re


DEFAULT_CONFIG_PATH = 'config/application.yml'


class ParameterNotFoundException(Exception):
    pass


class ParameterIllegalException(Exception):
    pass


class Configuration:

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.globel_app_conf = util.load_yaml(path)

    def prop(self, want):
        wants = re.split('\.', want)
        end = self.globel_app_conf
        for key in wants:
            if key in end:
                end = end[key]
            else:
                what = 'Path [%s] not found in application.yml' % want
                raise ParameterNotFoundException(what)
        return end


APP_SETTINGS = Configuration()

LOGGING_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'WARN': logging.WARN,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}

global status
status = {
    'val': 0
}
