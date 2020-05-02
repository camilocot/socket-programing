# chat server using multicast
# send.py
# usage : $ python send.py message

import socket
import struct
import sys

message = sys.argv[1] if len(sys.argv) > 1 else 'message via multicast'

multicast_addr = '224.0.0.1'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.sendto(bytes(message, encoding='utf-8'), (multicast_addr, port))
sock.close()
