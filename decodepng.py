#!/usr/bin/python

png = 0x89504e470d0a
enc = 0xf1601c2c3e73

key = str(hex(png^enc))[2:].decode("hex")
print key

encfd = open("enc.png","rb")
data = encfd.read()
encfd.close()
size = len(data)

decfd=open("dec.png","wb")
j = 0

for i in data:
    decfd.write(chr(ord(i)^ord(key[j%6])))
    j+=1

decfd.close()
