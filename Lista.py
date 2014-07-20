import re


patt = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)")

f = open("lista.txt").readlines()
valores = []
saida = open("proxy1.txt","w")

for each in f:
   host, port = patt.findall(each)[0]
   valores.append("%s:%s" %(host, port))

for each in valores:
   print each
   saida.write("%s\n"%(each))
saida.close
