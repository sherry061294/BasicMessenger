import socket
import sys
import signal
import select
import struct
import sys

def handler(signum, frame):
    print( "Bye!" )
    s.close()
    sys.exit(0)

port = sys.argv[2]
#print(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', int(port)))

s.listen(10)
read_handles = [s]

signal.signal(signal.SIGINT, handler)

while True:
    readables, _, _ = select.select(read_handles,[], [])
    for socks in readables:
        if socks == s:
            conn, addr = s.accept()
            read_handles.append(conn)
            #print(addr)
        else:
            datalen = socks.recv(4,socket.MSG_WAITALL)
            if datalen:
                length = struct.unpack("!i", datalen)
                #print("length is: " + str(length[0]))
                data = socks.recv(length[0], socket.MSG_WAITALL)
                #if data:
                #   message.ParseFromString(data)
                #   print(message.name +": " + message.text)
                for connection in read_handles:
                    if socks != connection and s!=connection:
                        try:
                            datalen_sent=connection.send(datalen)
                            data_sent = connection.send(data)
                        except:
                            read_handles.remove(connection)
