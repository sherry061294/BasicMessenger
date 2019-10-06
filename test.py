import sys
import message_pb2
import socket
import struct
import select

message=message_pb2.IMmessage()

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

    
print(servername)
print(name)

print(PORT)

print(confidentialityKey)

print(authenticityKey)


#print(message.name)
#print(message.text)


    
