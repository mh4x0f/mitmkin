from re import findall
import logging
from sys import stdout
from scapy.all import hexdump

'''http://stackoverflow.com/questions/17035077/python-logging-to-multiple-log-files-from-different-classes'''
def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.StreamHandler(stdout)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    l.setLevel(logging.INFO)
    l.addHandler(fileHandler)

class PSniffer(object):
    ''' plugins data sniffers'''

    def filterPackets(self,pkt):
        ''' intercept packetes data '''
        raise NotImplementedError

    def get_http_headers(self,http_payload):
        ''' get header dict http request'''
        try:
            headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]
            headers = dict(findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', headers_raw))
        except:
            return None
        if 'Content-Type' not in headers:
            return None

        return headers

    def hexdumpPackets(self,pkt):
        ''' show packets hexdump '''
        return hexdump(pkt)

    def makeLogger(self):
        ''' create logger save output sniffers'''
        setup_logger('pumpkinSniffer','pumpkinSniffer.log')
        self.logging = logging.getLogger('pumpkinSniffer')