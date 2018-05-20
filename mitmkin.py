
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from logging import getLogger,ERROR
getLogger('scapy.runtime').setLevel(ERROR)
import argparse
import sys
import signal
from core.main import CoreMitm
from core.utility.printer import banner, setcolor

_author  = ('{}'.format(setcolor('@mh4x0f',color='yellow')))
_version = setcolor('0.1',color='yellow')

def signal_handler(signal, frame):
    sys.exit(0)
banner()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="mitmkin - moduled sniffer for man-in-the-middle attack")
    parser.add_argument('-i','--interface',  dest='interface',help='set the interface to sniffing',default=None)
    parser.add_argument('-f','--filter',  dest='filter',help='set the filter packets',default='tcp and ( port 80 )')
    parser.add_argument('-v','--version', action='version', dest='version',version='%(prog)s v{}'.format(_version))
    sniffer = CoreMitm(parser.parse_args())
    print('Author: {} P0cL4bs Team'.format(_author))
    print('Version: {} dev\n'.format(_version))
    print('[*] Starting mitmkin...')
    print('[*] Berkeley packet filter:: [{}]'.format(sniffer.filter))
    print('Press Ctrl+C to exit')
    signal.signal(signal.SIGINT, signal_handler)
    sniffer.run()
    signal.pause()
