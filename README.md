## Simple Sniffer

### Prerequisites

- Python 3.6+
- tcpdump 4.99.1
- scapy 2.4
- PySide 6.2

**NOTE: Fully tested on Arch Linux, but should work well on other Linux distributions and Windows.**

### Features

- 

### Usage

```shell
python3 -m venv --copies venv
source venv/bin/activate
pip install -r requirements.txt
chmod 500 ./venv/bin/python3
sudo setcap cap_net_raw+eip ./venv/bin/python3
python3 -m simplesniffer
```

