#!/usr/bin/python

check = [0,4,6,0,6,0,0,5,6,3,0,5,6,9,2,5]
key = ""

for i in range(16):
        for j in range(10):
                if i*j % 10 == check[i]:
                        key += str(j)
                        break
print key
