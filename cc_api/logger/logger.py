import logging.config
import os


class Logger():
    def __init__(self):
        self.console = self.get_logger('console').exception
        self.debug = self.get_logger('debug').debug
        self.info = self.get_logger('info').info
        self.warning = self.get_logger('info').warning
        self.error = self.get_logger('error').error
        self.exception = self.get_logger('error').exception

    def get_logger(self, logger_name):
        config_path = os.path.join(os.path.dirname(__file__), 'logger.ini')
        logging.config.fileConfig(config_path)
        logger = logging.getLogger(logger_name)
        return logger


logger = Logger()
