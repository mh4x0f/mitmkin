# mitmkin
this is my sniffer for pumpkin module (scapy)

#### Description
A proxy that you can place between in a TCP stream. It filters the request and response streams with (scapy module) and actively modify packets of a TCP protocol that gets intercepted by tool. this plugin uses modules to view or modify the intercepted data that possibly easiest implementation of a module, just add your custom module on "core/plugins/".

```
mh4x0f@0xfl4bs:~/Developer/mitmkin$ sudo python mitmkin.py -h


            _ _             _    _
  _ __ ___ (_) |_ _ __ ___ | | _(_)_ __
 | '_ ` _ \| | __| '_ ` _ \| |/ / | '_ \.
 | | | | | | | |_| | | | | |   <| | | | |
 |_| |_| |_|_|\__|_| |_| |_|_|\_\_|_| |_|


usage: mitmkin.py [-h] [-i INTERFACE] [-f FILTER] [-v]

mitmkin - moduled sniffer for man-in-the-middle attack

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        set the interface to sniffing
  -f FILTER, --filter FILTER
                        set the filter packets
  -v, --version         show program's version number and exit
```

#### Instalation
```
$ sudo pip install scapy
$ sudo pip install BeautifulSoup
```

#### Plugin Dev

``` python
from scapy.all import *
from scapy_http import http # for layer HTTP
from plugin import PSniffer # base plugin class

class ExamplePlugin(PSniffer):
    _activated     = False
    _instance      = None
    meta = {
        'Name'      : 'Example',
        'Version'   : '1.0',
        'Description' : 'Brief description of the new plugin',
        'Author'    : 'your name',
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value

    @staticmethod
    def getInstance():
        if ExamplePlugin._instance is None:
            ExamplePlugin._instance = ExamplePlugin()
        return ExamplePlugin._instance

    def filterPackets(self,pkt): # (pkt) object in order to modify the data on the fly
        if pkt.haslayer(http.HTTPRequest): # filter only http request

            http_layer = pkt.getlayer(http.HTTPRequest) # get http fields as dict type
            ip_layer = pkt.getlayer(IP)# get ip headers fields as dict type

            print http_layer.fields['Method'] # show method http request
            # show all item in Header request http
            for item in http_layer.fields['Headers']:
                print('{} : {}'.format(item,http_layer.fields['Headers'][item]))

            print ip_layer.fields['src'] # show source ip address
            print ip_layer.fields['dst'] # show destiny ip address

            print http_layer # show item type dict
            print ip_layer # show item type dict


```

#### Overview
First of all you need to import two modules
``` python
from scapy.all import *
from plugin import PSniffer # base plugin class
```
the basic plugin example:

``` python
from scapy.all import *
from scapy_http import http # for layer HTTP
from plugin import PSniffer # base plugin class

class ExamplePlugin(PSniffer):
    _activated     = False
    _instance      = None
    meta = {
        'Name'      : 'Example',
        'Version'   : '1.0',
        'Description' : 'Brief description of the new plugin',
        'Author'    : 'your name',
    }
    def __init__(self):
        for key,value in self.meta.items():
            self.__dict__[key] = value

    @staticmethod
    def getInstance():
        if ExamplePlugin._instance is None:
            ExamplePlugin._instance = ExamplePlugin()
        return ExamplePlugin._instance

    def filterPackets(self,pkt): # (pkt) object in order to modify the data on the fly
        if pkt.haslayer(http.HTTPRequest): # filter only http request

            http_layer = pkt.getlayer(http.HTTPRequest) # get http fields as dict type
            ip_layer = pkt.getlayer(IP)# get ip headers fields as dict type

            print http_layer.fields['Method'] # show method http request
            # show all item in Header request http
            for item in http_layer.fields['Headers']:
                print('{} : {}'.format(item,http_layer.fields['Headers'][item]))

            print ip_layer.fields['src'] # show source ip address
            print ip_layer.fields['dst'] # show destiny ip address

            print http_layer # show item type dict
            print ip_layer # show item type dict



```

#### Packet function
You can modify any packet/protocol on the fly using Scapy. All packets pass through function **filterPackets** as you can see bellow. [read more about scapy](http://www.secdev.org/projects/scapy/doc/usage.html)
``` python
    def filterPackets(self,pkt): TCP packets layers
       print pkt.show() # show all details from packets
```

#### Logging
the Logging tab receive the dict object , where the key is name of plugin and the value is data. I will soon add other protocols, :+1:
