import sys
import message_pb2
import socket
import struct
import select

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
        message.text = keyboardInput
        message.name=name
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
                print(message.name +": " + message.text)
        



#print(servername)
#print(message.name)
#print(message.text)


    
