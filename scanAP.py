#!/usr/bin/env python
 
import sys
from scapy.all import *
 
interface = sys.argv[1]
aps = []

result = []

def sniffBeacon(p):
   if ( (p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) and not aps): 
 	print "Wireless Scanning ...."
 	print "SSID | BSSID | Channel | Encryption"
 	ssid  	= p[Dot11Elt].info
 	bssid 	= p[Dot11].addr3
	channel 	= int(ord(p[Dot11Elt:3].info))
	capability	= p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%} {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
 	
	if re.search("privacy", capability):
		if re.search("IBSS", capability):
 			enc = "WEP"
		else:
 			enc = "WPA"      
	else: enc  = 'Open'
	aps.append(p[Dot11].addr3)
	print ssid,"|",bssid,"|",channel,"|",enc

sniff(iface=interface,prn=sniffBeacon,timeout=10)
print aps
