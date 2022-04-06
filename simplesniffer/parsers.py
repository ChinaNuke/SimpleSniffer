import logging
import re
from collections import OrderedDict

import scapy.all as scapy

logger = logging.getLogger(__name__)


class PacketParser(object):
    def __init__(self) -> None:
        pass

    # 直接解析scapy show函数的输出
    def parse(self, pkt) -> OrderedDict:
        result = OrderedDict()
        output = pkt.show(dump=True)
        logger.debug(output)

        '''
        result: {
            'Ethernet': [
              'dst=xxxx',
              'src=xxx'
            ],
            'IPv6': [
                'version=6',
                ...
            ],
            'IPv6 Extension Header': [
                'nh=ICMPv6',
                ...,
                'options': {
                    'Router Alert': [
                        'otype=xxx',
                        'optlen=xxx'
                    ],
                    'PadN': [
                        'otype=xxx'
                    ]
                }
            ]
        }
        '''

        # 先实现一个最简单的逻辑
        current_layer_name = None
        current_options_name = None
        current_options = None  # OrderedDict()
        current_option = None
        for line in output.splitlines():
            # logger.debug(f'current line: {line.strip()}')
            if line.startswith('###'):  # [ Ethernet ]###
                current_layer_name = re.search(
                    r'###\[\s(.*?)\s\]###', line).group(1)
                result[current_layer_name] = []
            elif line.strip().startswith('\\'):  # \qd        \
                current_options_name = re.search(r'\\(.*?)\s', line).group(1)
                current_options = OrderedDict()
                current_options[current_options_name] = {}
                result[current_layer_name].append(current_options)
            # |###[ DNS Question Record ]###
            elif line.strip().startswith('|#'):
                current_option = re.search(
                    r'\|###\[\s(.*?)\s\]###', line).group(1)
                current_options[current_options_name][current_option] = []
            elif line.strip().startswith('|'):
                current_options[current_options_name][current_option].append(
                    line.strip()[3:])  # remove the '|  ' prefix
            else:
                result[current_layer_name].append(line.strip())

        # logger.debug(result)
        return result

    def hexdump(self, pkt):
        return scapy.hexdump(pkt, dump=True)
