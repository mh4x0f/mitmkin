import urllib
import threading
import time
import socket
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

    def cancel(self):
        self.stop_down = True
if __name__ == "__main__":
    url = "https://dl.dropboxusercontent.com/u/97321327/chrome/sqlite3.dll"
    down = Downloader()
    down.download(url, "sqlite3.dll")
    print "Download started..."
    time.sleep(20)
    down.cancel()
    print "Download cancelado"

