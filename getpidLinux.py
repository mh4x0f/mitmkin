import os 
from re import search
comando = os.popen("tasklist")
nes = comando.readlines()
print nes[4]
i = 0
while i < 200:
	i = i +1 
	if search("4820", nes[i]):
		print("ta funcionando!")
		print(nes[i])
		exit(1)
	else:
		print("nao tem esse processo")
		print(nes[i])
		
