# ping/pong server using multicast
# receiver.py
# usage : $ python receiver.py  # wait for messages to come in

import socket
import struct
import sys

multicast_addr = '224.0.0.1'

port = 3000
server_address = ('', port)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_addr)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Receive/respond loop
while True:
    data, address = sock.recvfrom(1024)

    print('received: %s with length %s bytes, data' % (data, len(data)))
    print('sending acknowledgement to {}'.format(address))

    sock.sendto(b'ack', address)
