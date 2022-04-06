import logging
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

        self.sniffer = scapy.AsyncSniffer(
            iface=self.iface, 
            filter=self.filter,
            prn=self._handle_packet, 
            # stop_filter=lambda _: self.stop_flag, 
            store=False
        )

        self.buffer = []

    # https://stackoverflow.com/questions/13549294/get-all-the-layers-in-a-packet
    def _getlayers(self, pkt):
        layers = []
        counter = 0
        while True:
            layer = pkt.getlayer(counter)
            if not layer:
                break
            layers.append(layer)
            counter += 1
        return layers

    @Slot()
    def run(self):
        logger.debug('sniffer starts to run...')
        self.stop_flag = False
        try:
            # About how to stop sniffing:
            # https://github.com/secdev/scapy/issues/989
            # scapy.sniff(
            #     iface=self.iface, 
            #     filter=self.filter,
            #     prn=self._handle_packet, 
            #     stop_filter=lambda _: self.stop_flag, 
            #     store=False
            # )
            # while not self.stop_flag:
            #     # logger.debug('running...')
            #     sleep(1)

            # i think it's better to use AsyncSniffer
            self.sniffer.start()

        except BaseException as e:
            logger.error(f'Unexcepted error: {e}')
            self.finished.emit()

    def quit(self):
        logger.warning('stop_flag is set.')
        self.stop_flag = True
        self.sniffer.stop()
        self.finished.emit()

    def get_packet(self, index):
        return self.buffer[index]

    def _handle_packet(self, pkt):
        self.buffer.append(pkt)

        layers = self._getlayers(pkt)
        src, dst = layers[0].src, layers[0].dst
        # logger.debug(f'src: {src}, dst: {dst}')

        for layer in layers:
            if layer.name not in ['Raw', 'Padding']:
                name = layer.name
            try:
                src, dst = layer.src, layer.dst
            except AttributeError as e:
                pass
        
        # TODO: check if dport is http_www
        # TODO: complete the summary fields
        # TODO: add length field
        summary = (str(self.counter), 'timestamp', src or '', dst or '', name or '', 'test2')
        self.new_packet.emit(summary)
        
        self.counter += 1

        

        # https://scapy.readthedocs.io/en/latest/api/scapy.packet.html
        # haslayer
        # firstlayer
        # lastlayer
        # layers
