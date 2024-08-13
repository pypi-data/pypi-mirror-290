import logging


class Logger:
    def __init__(self, name, level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        self.logger = Logger.setup_logger(name, level, format)

    @staticmethod
    def setup_logger(name, level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
        """
        Setup and return a logger with the specified name and level.

        :param name: Name of the logger.
        :param level: Logging level, e.g., logging.INFO or logging.DEBUG.
        :param format: Format string for log messages.
        :return: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:  # Ensure no duplicate handlers are added
            handler = logging.StreamHandler()
            formatter = logging.Formatter(format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)
