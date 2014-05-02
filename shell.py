#!/usr/bin/python
 

 
import sys
 
if len(sys.argv) != 2:
    print 'python shell.py $\'shellcode\''
    sys.exit()
 
shellcode = (sys.argv[1])
encoded = ""
 
print '[+] shellcode enconde para XOR'
print '[+] chmodsecurity'
 
if len(shellcode) % 2 != 0:
    print '[+] Adicionando PON para uniformizar shellcode...'
    shellcode += ("\x90")
 
print '[+] Encoding...'
 
byteA = ""
counter = 0
 
for x in bytearray(shellcode):
    if counter % 2 == 0:
        byteA = x
    else:
        y = ~x
        y = y & 0xff
        XORByte = byteA^y
        NOTByte = y
        encoded += '0x'
        encoded += '%02x,' % XORByte
        encoded += '0x'
        encoded += '%02x,' % NOTByte
 
    counter += 1
 
print '[+] Encoded Shellcode: ' + encoded + '0xff,0xff'
print '[+] msfc0d3r!'
f = open("shellcode.txt","w")
f.write(encoded + '0xff,0xff')
f.close
