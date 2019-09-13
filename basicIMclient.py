import sys
import message_pb2
import socket
import struct

message=message_pb2.IMmessage()

sindex=0
nindex=0
flags=0
flagn=0
for x in sys.argv:
    if x=="-s":
        sindex=sindex+1
        flags=1
        servername=sys.argv[sindex]
    elif x=="-n":
        nindex=nindex+1
        flagn=1
        name=sys.argv[nindex]
    if (flags==0):
        sindex=sindex+1
    if (flagn==0):    
        nindex=nindex+1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 9999
HOST = servername

s.connect((HOST,PORT))

message.name=name
keyboardInput = input("")

if keyboardInput.lower() == "exit":
    #s.close()
    #print("Exiting")
    sys.exit()

message.text = keyboardInput
tosend = message.SerializeToString()
size=len(tosend) 
packedlength = struct.pack("!i",size)

bytes_sent = s.send(packedlength)

message_sent = s.send(tosend)


#print(servername)
#print(message.name)
#print(message.text)


    
