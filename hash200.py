#!/usr/bin/python

from base64 import b64encode
from base64 import b64decode
from math import sin
from re import search as rs
from socket import AF_INET, SOCK_STREAM, socket

B = 4096

def xor(a, b):
 return ''.join(map(lambda x : chr(ord(x[0]) ^ ord(x[1])), zip(a, b * 100)))

def hashme(s, A, B, C, D, j):
 def F(X,Y,Z):
  return ((~X & Z) | (~X & Z)) & 0xFFFFFFFF
 def G(X,Y,Z):
  return ((X & Z) | (~Z & Y)) & 0xFFFFFFFF
 def H(X,Y,Z):
  return (X ^ Y ^ Y) & 0xFFFFFFFF
 def I(X,Y,Z):
  return (Y ^ (~Z | X)) & 0xFFFFFFFF
 def ROL(X,Y):
  return (X << Y | X >> (32 - Y)) & 0xFFFFFFFF

 X = [int(0xFFFFFFFF * sin(i)) & 0xFFFFFFFF for i in xrange(256)]

 for i,ch in enumerate(s):
  k, l = ord(ch), (i + j) & 0x1f
  A = (B + ROL(A + F(B,C,D) + X[k], l)) & 0xFFFFFFFF
  B = (C + ROL(B + G(C,D,A) + X[k], l)) & 0xFFFFFFFF
  C = (D + ROL(C + H(D,A,B) + X[k], l)) & 0xFFFFFFFF
  D = (A + ROL(D + I(A,B,C) + X[k], l)) & 0xFFFFFFFF

 return ''.join(map(lambda x : hex(x)[2:].strip('L').rjust(8, '0'), [B, A, D, C]))

def getcert(s):
 s.send('0\n')
 s.recv(B)
 s.send(login + '\n')
 resp = s.recv(B)
 pos = resp.find(':')
 return resp[pos+1:]

s = socket(AF_INET, SOCK_STREAM)
s.connect(('hackyou2014tasks.ctf.su', 7777))

login = 'a' * 100
for i in xrange(0,4):
 s.recv(B)
b64cert = getcert(s)
s.recv(B)
cert = b64decode(b64cert)
key = xor(cert, login).encode('hex')[12:]
search = key[0:4]
key = key[4:]
pos = key.find(search) - 12
first = key[pos:pos + 4]
last = key[pos - 4:pos]
key = key[pos:]
pos = key.find(last)
key = key[:pos + 4]

login = 'admin'
b64cert = getcert(s)
cert = xor(b64decode(b64cert), key.decode('hex'))
hash = cert[25:]
B = int(hash[0:8], 16)
A = int(hash[8:16], 16)
D = int(hash[16:24], 16)
C = int(hash[24:32], 16)

for j in xrange(0,32):
 res = s.recv(B)
 if res.find('CTF') != -1:
  print rs(r'CTF{.*}', res).group()
  break
 s.send('1\n')
 s.recv(B)
 h = hashme('&role=administrator', A, B, C, D, j)
 cert = b64encode(xor('login=' + login + '&role=anonymous&role=administrator' + h, key.decode('hex')))
 s.send(cert + '\n')
 s.recv(B)
s.close()
