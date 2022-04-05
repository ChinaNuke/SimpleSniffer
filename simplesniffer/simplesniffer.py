"""Main entry for simplesniffer.

Usage: python3 -m simplesniffer -h

"""

import argparse
import logging
import scapy.all as scapy
import signal
import sys

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QTableWidgetItem
from simplesniffer.log import configure_logger
from simplesniffer.gui.mainwindow import Ui_MainWindow
from simplesniffer.sniffer import Sniffer

logger = logging.getLogger(__name__)    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_interfaces()
        self.ui.btnStop.setDisabled(True)

        self.ui.btnStart.clicked.connect(self.start_sniffing)
        self.ui.btnStop.clicked.connect(self.stop_sniffing)

        self.ui.statusbar.showMessage('Ready!')

    def init_interfaces(self):
        # TODO: 是否移到单独的文件中？
        interfaces = scapy.get_if_list()
        self.ui.comboNIC.addItems(interfaces)

    @Slot()
    def update_flowtable(self, summary):
        logger.debug(summary)
        row_num = self.ui.tblFlows.rowCount()
        self.ui.tblFlows.insertRow(row_num)
        for i in range(6):
            self.ui.tblFlows.setItem(row_num, i, QTableWidgetItem(summary[i]))
        if self.ui.tblFlows.NoSelection:
            self.ui.tblFlows.scrollToBottom()

    @Slot()
    def update_details(self):
        pass

    @Slot()
    def start_sniffing(self):
        filter_text = self.ui.txtFilter.text
        iface = 'wlp60s0'

        # https://realpython.com/python-pyqt-qthread/
        self.thread = QThread()
        self.worker = Sniffer(iface, '')
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.new_packet.connect(self.update_flowtable)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        self.ui.btnStop.setDisabled(False)
        self.ui.btnStart.setDisabled(True)
        self.ui.statusbar.showMessage('Sniffing started!')

    @Slot()
    def stop_sniffing(self):
        self.worker.quit()

        self.ui.btnStop.setDisabled(True)
        self.ui.btnStart.setDisabled(False)
        self.ui.statusbar.showMessage('Sniffing finished!')


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
    logger.warning('Exiting...')
    stop_flag = True
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, exit)
    args = parse_arguments()

    # Configure logger
    configure_logger(stream_level='DEBUG' if args.debug else 'INFO')

    logger.debug('hello!')

    # https://scapy.readthedocs.io/en/latest/routing.html
    # interfaces = scapy.get_if_list()
    # logger.debug(f'All network interfaces available: {interfaces}') # ['lo', 'enp59s0', 'wlp60s0', 'vmnet1', 'vmnet8']
    
    # result = scapy.sniff(iface='wlp60s0', filter='icmp', count=10, prn=lambda x: logger.debug(x.summary()))
    # result.show()
    # logger.info(result)

    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()

    logger.debug('hello again!')

    sys.exit(app.exec())


# https://scapy.readthedocs.io/en/latest/usage.html
# https://doc.qt.io/qtforpython/tutorials/index.html
# https://github.com/PENGZhaoqing/SimpleSniff
# https://www.cnblogs.com/rogunt/p/16030357.html
# https://www.pythonguis.com/faq/pyqt6-vs-pyside6/
# https://github.com/feeluown/FeelUOwn
# https://blog.l0v0.com/posts/bea01990.html