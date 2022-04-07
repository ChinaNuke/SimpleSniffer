import logging
from datetime import datetime

import scapy.all as scapy
from PySide6.QtCore import QObject, QThread, Signal, Slot

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

        time = datetime.fromtimestamp(pkt.time).strftime('%Y-%m-%d %H:%M:%S')
        length = len(pkt)
        layers = self._getlayers(pkt)
        info = None

        # 获取最上层的地址和协议信息，考虑了嵌套的情况，
        # 比如使用IP隧道的数据包有多个IP层，则读取最外层的信息
        for layer in layers:
            if layer.name not in ('Raw', 'Padding'):
                protocol = layer.name
            try:
                src, dst = layer.src, layer.dst
            except AttributeError as e:
                pass

        # 对于一些常见的协议进行解析提取部分头信息，并重写protocol解析结果
        if pkt.haslayer(scapy.TCP):
            if pkt.dport == 80 or pkt.sport == 80:
                protocol = 'HTTP'
                if pkt.haslayer(scapy.Raw):
                    info = pkt[scapy.Raw].load.split(b'\r\n')[0].decode()
                else:
                    info = 'HTTP'
            elif pkt.dport == 443 or pkt.sport == 443:
                protocol = 'HTTPS'
                info = 'HTTPS (Encrypted)'
            # elif pkt.proto == 1:
            #     protocol = 'ICMP'
            elif pkt.dport == 21 or pkt.sport == 21:
                protocol = 'FTP'
            elif pkt.dport == 22 or pkt.sport == 22:
                protocol = 'SSH'
            else:
                logger.debug('TCP')
                info = pkt.sprintf(
                    '%r,TCP.sport% -> %r,TCP.dport% [%TCP.flags%] '
                    'Seq=%TCP.seq% Ack=%TCP.ack% Win=%TCP.window%'
                )
            # logger.debug(f'info: {info}')

        # 兜底情况
        if not info or info == '':
            if layers[-1].name not in ('Raw', 'Padding'):
                info = layers[-1].summary()
            else:
                info = layers[-2].summary()

        summary = (str(self.counter), time, src,
                   dst, protocol, str(length), info)
        self.new_packet.emit(summary)

        self.counter += 1
