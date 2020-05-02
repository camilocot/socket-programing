# ping/pong client using multicast
# send.py
# usage : $ python send.py message

import socket
import struct
import sys

message = sys.argv[1] if len(sys.argv) > 1 else 'ping via multicast'

multicast_addr = '224.0.0.1'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)
# Multicast datagrams are sent with a default TTL value of 1, to prevent them to be forwarded beyond the local network.
# and flooding network segments
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


try:

    # Send data to the multicast group
    print('sending "%s"' % message)
    sock.sendto(bytes(message, encoding='utf-8'), (multicast_addr, port))

    # Look for responses from all recipients
    while True:
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses', file=sys.stderr)
            break
        else:
            print('received "%s" from %s' % (data, server))

finally:
    sock.close()
