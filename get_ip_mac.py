import subprocess
import sys
remotehost= sys.argv[1]
def get_ip_mac(remotehost):
	cmd="arp -a"
	p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	output, errors = p.communicate()
	if output is not None :
    		if sys.platform in ['linux','linux2']:
        		for i in output.split("\n"):
            			if remotehost in i:
                			for j in i.split():
                    				if ":" in j:
                       					 print "%s--> %s" % (remotehost,j)
				else:
					print('no response form %s'%(j))

get_ip_mac(remotehost)
