"""Main entry for simplesniffer.

Usage: python3 -m simplesniffer -h

"""

import argparse
import logging
import scapy.all as scapy
import signal
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from simplesniffer.log import configure_logger
from simplesniffer.gui.mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def parse_arguments(arguments=None):
    """Parse the SimpleSniffer arguments.
    Args:
        arguments: the arguments, optionally given as argument.
    Returns:
        a Namespace object.
    """

    parser = argparse.ArgumentParser(description='SimpleSniffer')

    parser.add_argument('--debug', action='store_true',
                        help='show debugging informations')

    return parser.parse_args(args=arguments)


def exit(sig, frame):
    global stop_flag
    print('Exiting...')
    stop_flag = True
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, exit)
    args = parse_arguments()

    # Configure logger
    configure_logger(stream_level='DEBUG' if args.debug else 'INFO')
    logger = logging.getLogger(__name__)

    logger.debug('hello!')

    # app = QtWidgets.QApplication([])

    # widget = MainWindow()
    # widget.resize(300, 200)
    # widget.show()

    interfaces = scapy.get_if_list()
    logger.debug(f'All network interface cards available: {interfaces}')

    logger.debug('hello again!')

    # sys.exit(app.exec())

    logger.debug('exited!')
