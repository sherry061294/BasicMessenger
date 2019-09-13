import socket
import message_pb2
import sys
import signal

def handler(signum, frame):
    print( "Bye!" )
    s.close()
    sys.exit(0)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctr=0
s.bind(('', 9999))

s.listen(10)
try:
    conn[ctr], addr[ctr] = s.accept()
    ctr=ctr+1

    read_handles = [sys.stdin, conn[]]
    signal.signal(signal.SIGINT, handler)
                    
except KeyboardInterrupt:
    s.close()
    sys.exit()
