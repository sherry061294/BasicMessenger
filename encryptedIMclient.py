import sys
import message_pb2
import socket
import struct
import select
import hashlib
from Crypto.Random import get_random_bytes 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

message=message_pb2.IMmessage()

def encrypting(data, ckey, IV):
    data = data.encode('utf-8')
    aes = AES.new(ckey, AES.MODE_CBC, IV)
    ciphertext = aes.encrypt(pad(data,16))
    return ciphertext

def decrypting(ciphertext, ckey, IV):
    aes = AES.new(ckey, AES.MODE_CBC, IV)
    try:
        byte_plaintext = unpad(aes.decrypt(ciphertext),16)
    except:
        return -1
    return byte_plaintext.decode('utf-8')

#def Macing(self, data, key):
    
        
def main():
    sindex=0
    nindex=0
    pindex=0
    cindex=0 #for confidentiality key
    aindex=0 # for authenticity key
    flags=0
    flagn=0
    flagp=0
    flagc=0
    flaga=0

    for x in sys.argv:
        if x=="-s":
            sindex=sindex+1
            flags=1
            servername=sys.argv[sindex]
        elif x=="-n":
            nindex=nindex+1
            flagn=1
            name=sys.argv[nindex]
        elif x=="-p":
            pindex=pindex+1
            flagp=1
            PORT=sys.argv[pindex]
        elif x=="-c":
            cindex=cindex+1
            flagc=1
            confidentialityKey=sys.argv[cindex]
        elif x=="-a":
            aindex=aindex+1
            flaga=1
            authenticityKey=sys.argv[aindex]
        if (flags==0):
            sindex=sindex+1
        if (flagn==0):    
            nindex=nindex+1
        if (flagp==0):    
            pindex=pindex+1
        if (flagc==0):    
            cindex=cindex+1
        if (flaga==0):    
            aindex=aindex+1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = servername
    hashed_authenticityKey = hashlib.sha256(authenticityKey.encode('utf-8')).digest()
    hashed_confidentialityKey = hashlib.sha256(confidentialityKey.encode('utf-8')).digest()
    #print(len(hashed_confidentialityKey))

    s.connect((HOST,int(PORT)))
    #print("Connected")

    read_handles = [ sys.stdin, s ]

    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])
        if sys.stdin in ready_to_read_list:
            keyboardInput = input("")
            if keyboardInput.lower() == "exit":
                s.close()
                #print("Exiting")
                sys.exit()
            message.nameIV = get_random_bytes(16)
            message.name = encrypting(name, hashed_confidentialityKey, message.nameIV)
            message.textIV = get_random_bytes(16)
            message.text = encrypting(keyboardInput, hashed_confidentialityKey, message.textIV)
            tosend = message.SerializeToString()
            size=len(tosend) 
            packedlength = struct.pack("!i",size)
            bytes_sent = s.send(packedlength)
            message_sent = s.send(tosend)
        if s in ready_to_read_list:
            datalen = s.recv(4,socket.MSG_WAITALL)
            if datalen:
                length = struct.unpack("!i", datalen)
                msglen = length[0]
                #print("length is: " + str(length[0]))
                data = s.recv(length[0], socket.MSG_WAITALL)
                if data:
                    message.ParseFromString(data)
                    received_name = decrypting(message.name, hashed_confidentialityKey, message.nameIV)
                    received_text = decrypting(message.text, hashed_confidentialityKey, message.textIV)
                    if (received_name == -1 or received_text == -1):
                        print("Incorrect Key")
                    else:
                        print( "%s: %s" % (received_name, received_text), flush=True )
            



    #print(servername)
    #print(message.name)
    #print(message.text)

if __name__== "__main__":
    main()
    
