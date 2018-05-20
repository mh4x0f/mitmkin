import zlib
from random import randint
from scapy.all import *
from plugin import PSniffer

class ImageCap(PSniffer):
    ''' capture image content http'''
    _name          = 'ImageCap'
    _activated     = False
    _instance      = None

    @staticmethod
    def getInstance():
        if ImageCap._instance is None:
            ImageCap._instance = ImageCap()
        return ImageCap._instance
    def __init__(self):
        self.makeLogger()

    def filterPackets(self,pkt):
        if pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP):
            if pkt[TCP].dport == 80 or pkt[TCP].sport == 80:
                try:
                    self.http_payload = str(pkt[TCP].payload)
                except: pass
                self.headers = self.get_http_headers(self.http_payload)
                if self.headers != None:
                    # extract the raw image and return the image type and the binary body of
                    # the image itself
                    image, image_type = self.extract_image(self.headers, self.http_payload)
                    if image is not None and image_type is not None:

                        file_name = 'TESTE%s.%s' %(self.random_char(5), image_type)
                        fd = open('image/%s' % (file_name), 'wb')
                        fd.write(image)
                        fd.close()

    def random_char(self,y):
           return ''.join(random.choice(string.ascii_letters) for x in range(y))

    def extract_image(self,headers, http_payload):
        image,image_type = None, None
        try:
            if 'image' in headers['Content-Type']:
                image_type = headers['Content-Type'].split('/')[1]
                image = http_payload[http_payload.index('\r\n\r\n')+4:]
                try:
                    if 'Content-Encoding' in headers.keys():
                        if headers['Content-Encoding'] == 'gzip':
                            image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                        elif headers['Content-Encoding'] == 'deflate':
                            image = zlib.decompress(image)
                except:
                    pass
        except:
            return None, None
        return image, image_type
