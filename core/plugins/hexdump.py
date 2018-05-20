from scapy.all import *
from plugin import PSniffer
import sys
from io import StringIO

class Hexdump(PSniffer):
    ''' print dump packets http POST  hex '''
    _name          = 'Hexdump'
    _activated     = False
    _instance      = None

    @staticmethod
    def getInstance():
        if Hexdump._instance is None:
            Hexdump._instance = Hexdump()
        return Hexdump._instance

    def __init__(self):
        self.makeLogger()

    def filterPackets(self,pkt):
        if pkt.haslayer(Ether) and pkt.haslayer(Raw) and not pkt.haslayer(IP) and not pkt.haslayer(IPv6):
            return
        if pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):
            self.load = pkt[Raw].load
            if self.load.startswith('POST'):
                hexdump(self.load)



def hexdump( src, length=16, sep='.' ):
	'''
	https://gist.github.com/ImmortalPC/c340564823f283fe530b
	@brief Return {src} in hex dump.
	@param[in] length	{Int} Nb Bytes by row.
	@param[in] sep		{Char} For the text part, {sep} will be used for non ASCII char.
	@return {Str} The hexdump
	@note Full support for python2 and python3 !
	'''
	result = [];

	# Python3 support
	try:
		xrange(0,1);
	except NameError:
		xrange = range;

	for i in xrange(0, len(src), length):
		subSrc = src[i:i+length];
		hexa = '';
		isMiddle = False;
		for h in xrange(0,len(subSrc)):
			if h == length/2:
				hexa += ' ';
			h = subSrc[h];
			if not isinstance(h, int):
				h = ord(h);
			h = hex(h).replace('0x','');
			if len(h) == 1:
				h = '0'+h;
			hexa += h+' ';
		hexa = hexa.strip(' ');
		text = '';
		for c in subSrc:
			if not isinstance(c, int):
				c = ord(c);
			if 0x20 <= c < 0x7F:
				text += chr(c);
			else:
				text += sep;
		result.append(('%08X:  %-'+str(length*(2+1)+1)+'s  |%s|') % (i, hexa, text));

	return '\n'.join(result);
