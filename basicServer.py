import sys
import message_pb2
import socket
import struct
message=message_pb2.IMmessage()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', 9999))
s.listen(1)

conn, addr = s.accept()
# if we got here, then someone is talking to us.
# (we could accept another connection by calling
# s.accept() again, but we won't do that in this example)

print('Connected by', addr)

data = conn.recv(4,socket.MSG_WAITALL)
if data:
    length = struct.unpack("!i", data)
    msglen = length[0]
    print("length is: " + str(length[0]))

data = conn.recv(length[0], socket.MSG_WAITALL)
if data:
    message.ParseFromString(data)
    print(message.name +": " + message.text)
    
    
