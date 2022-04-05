import logging
from time import sleep
import scapy.all as scapy

from PySide6.QtCore import QThread, QObject, Signal, Slot

logger = logging.getLogger(__name__)


class Sniffer(QObject):

    finished = Signal()
    new_packet = Signal(tuple)

    def __init__(self, iface, filter):
        super().__init__()
        self.iface = iface
        self.filter = filter
        self.stop_flag = False
        self.counter = 0

    @Slot()
    def run(self):
        logger.debug('sniffer starts to run...')
        self.stop_flag = False
        try:
            # About how to stop sniffing:
            # https://github.com/secdev/scapy/issues/989
            scapy.sniff(
                iface=self.iface, 
                filter=self.filter,
                prn=self.handle_packet, 
                stop_filter=lambda _: self.stop_flag, 
                store=False
            )
            # while not self.stop_flag:
            #     logger.debug('running...')
            #     sleep(1)

            self.finished.emit()
        except BaseException as e:
            logger.error(f'Unexcepted error: {e}')
            self.finished.emit()

    def quit(self):
        logger.warning('stop_flag is set.')
        self.stop_flag = True

    def handle_packet(self, pkt):
        logger.debug('callback function is called.')
        logger.debug(pkt.summary())
        summary = (str(self.counter), 'test', pkt.src, pkt.dst, 'test3', 'test2')
        self.new_packet.emit(summary)
        self.counter += 1
