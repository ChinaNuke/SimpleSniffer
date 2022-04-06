"""Main entry for simplesniffer.

Usage: python3 -m simplesniffer -h

"""

import argparse
import logging
import sys
from typing import OrderedDict

import scapy.all as scapy
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Slot
from PySide6.QtWidgets import QTableWidgetItem, QTreeWidgetItem

from simplesniffer.gui.mainwindow import Ui_MainWindow
from simplesniffer.log import configure_logger
from simplesniffer.parsers import PacketParser
from simplesniffer.sniffer import Sniffer

logger = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_interfaces()
        self.init_flowtable()
        self.ui.btnStop.setDisabled(True)

        self.ui.btnStart.clicked.connect(self.start_sniffing)
        self.ui.btnStop.clicked.connect(self.stop_sniffing)

        self.ui.statusbar.showMessage('Ready!')

        self.parser = PacketParser()

    def init_interfaces(self):
        # TODO: 是否移到单独的文件中？
        interfaces = scapy.get_if_list()
        self.ui.comboNIC.addItems(interfaces)

        # set the default interface to wireless card
        for name in interfaces:
            if name.startswith('wl'):
                self.ui.comboNIC.setCurrentText(name)
                break

    def init_flowtable(self):
        self.ui.tblFlows.setColumnWidth(0, 30)  # No.
        self.ui.tblFlows.setColumnWidth(1, 80)  # Time
        self.ui.tblFlows.setColumnWidth(2, 160)  # Source
        self.ui.tblFlows.setColumnWidth(3, 160)  # Destination
        self.ui.tblFlows.setColumnWidth(4, 160)  # Protocol
        # self.ui.tblFlows.setColumnWidth(5, 200) # Info

        self.ui.tblFlows.currentItemChanged.connect(self.update_details)

    @Slot(tuple)
    def update_flowtable(self, summary):
        # logger.debug(summary)

        # insert a new row and fill up the columns
        row_num = self.ui.tblFlows.rowCount()
        self.ui.tblFlows.insertRow(row_num)
        for i in range(6):
            self.ui.tblFlows.setItem(row_num, i, QTableWidgetItem(summary[i]))

        if not self.ui.tblFlows.selectedItems():
            self.ui.tblFlows.scrollToBottom()

    @Slot(QTableWidgetItem, QTableWidgetItem)
    def update_details(self, current, previous):
        row = current.row()
        index = int(self.ui.tblFlows.item(row, 0).text())
        logger.debug(f'selected index: {index}')

        pkt = self.worker.get_packet(index)
        details = self.parser.parse(pkt)

        # 生成多级树结构
        # https://doc.qt.io/qtforpython/tutorials/basictutorial/treewidget.html
        # TODO: 算法多少有一些复杂，或许能简化一下
        items = []
        for layer, contents in details.items():
            layer_item = QTreeWidgetItem([layer])
            for content in contents:
                if isinstance(content, OrderedDict):
                    # must have only one keys
                    options_item = QTreeWidgetItem([list(content.keys())[0]])
                    for k, vs in list(content.values())[0].items():
                        option_item = QTreeWidgetItem([k])
                        for v in vs:
                            c = QTreeWidgetItem([v])
                            option_item.addChild(c)
                        options_item.addChild(option_item)

                    child = options_item
                else:
                    child = QTreeWidgetItem([content])
                layer_item.addChild(child)
            items.append(layer_item)

        self.ui.treeDetials.clear()
        self.ui.treeDetials.insertTopLevelItems(0, items)

    @Slot()
    def start_sniffing(self):
        filter_text = self.ui.txtFilter.text()
        iface = self.ui.comboNIC.currentText()

        # clean up the views
        self.ui.tblFlows.clear()
        self.ui.treeDetials.clear()

        # start a new thread to run the sniffer
        # https://realpython.com/python-pyqt-qthread/
        self.thread = QThread()
        self.worker = Sniffer(iface, filter_text)
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


def main():
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
