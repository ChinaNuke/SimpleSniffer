
"""Module for setting up logging."""
import logging
import sys

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO
}

LOG_FORMATS = {
    'DEBUG': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    'INFO': '[%(asctime)s] [%(levelname)s] %(message)s]'
}


class ColoredFormatter(logging.Formatter):
    """Custom logger formatter with colors."""

    # Get color codes
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = \
        [f'\x1b[1;{30+i}m' for i in range(8)]
    RESET = '\x1b[0m'

    COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: WHITE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA
    }

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt, style=style,
                                   validate=validate)

    def format(self, record):
        # Replace the original levelname with colored levelname
        levelname = record.levelname
        record.levelname = self.COLORS[record.levelno] + levelname + self.RESET
        return logging.Formatter.format(self, record)


def configure_logger(stream_level='INFO', debug_file=None):
    """Configure logging for simplesniffer.
    Set up logging to stdout with given level.
    """

    # Set up 'simplesniffer' logger
    logger = logging.getLogger("simplesniffer")
    logger.setLevel(logging.DEBUG)

    # Remove all attached handlers, in case there was a logger with using the
    # name 'simplesniffer'
    del logger.handlers[:]

    # Get settings based on the given stream_level
    # log_formatter = logging.Formatter(fmt=LOG_FORMATS[stream_level],
    #   datefmt='%H:%M:%S')
    log_formatter = ColoredFormatter(fmt=LOG_FORMATS[stream_level],
                                     datefmt='%H:%M:%S')
    log_level = LOG_LEVELS[stream_level]

    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger
