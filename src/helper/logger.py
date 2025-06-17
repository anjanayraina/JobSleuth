# helpers/logger.py
from loguru import logger
import sys

class Logger:
    def __init__(self, log_file="app.log"):
        logger.remove()  # Remove default handler
        logger.add(sys.stdout, level="DEBUG")
        logger.add(log_file, level="DEBUG", rotation="10 MB", retention="7 days")
        self.logger = logger

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

