from struct import *
import sys
import socket


def main():
    #  Address Family Packet. This is used when we want to capture and manipulate traffic
    # Raw packets are passed to and from the device driver without any changes in the packet data
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        ethernet_data, address = s.recvfrom(65536)
        dest_mac, src_mac, protocol, ip_data = ethernet_dissect(ethernet_data)
        print("\nEthernet Frame Captured:")
        print("Destination MAC Address: {} Source MAC Address: {} Protocol: {}".format(
            dest_mac, src_mac, protocol))

        # IPv4
        if protocol == 8:
            ip_protocol, source_ip, target_ip, ipdata = ipv4_packet(ip_data)
            print("\t[-] IP packet: Source IP: {} Destination IP: {}".format(
                source_ip, target_ip))
            if ip_protocol == 17:
                source, destination = udp_packet(ipdata)
                print("\t[-] UDP datagram: Source Port: {} Destination Port: {}".format(
                    source, destination))


def ethernet_dissect(data):

    dest_mac, src_mac, protocol = unpack('! 6s 6s H', data[:14])
    return mac_format(dest_mac), mac_format(src_mac), socket.htons(protocol), data[14:]


def ethernet_dissect(ethernet_data):

    # What we care about is the first 14 bytes which include the Destination MAC, the Source MAC and the Encapsulated protocol Type (0800 - IPv4)
    #! – The form ‘!’ is available for those poor souls who claim they can’t remember whether network byte order is big-endian or little-endian.
    # 6s – A string of 6 characters. MAC addresses are 48 bits or 6 bytes long
    # 6s – A string of 6 characters. MAC addresses are 48 bits or 6 bytes long
    # H – Unsigned short integer of 2 bytes.
    dest_mac, src_mac, protocol = unpack(
        '! 6s 6s H', ethernet_data[:14])
    # socket.htons(protocol) converts the protocol integers from host to network byte
    return mac_format(dest_mac), mac_format(src_mac), socket.htons(protocol), ethernet_data[14:]


def mac_format(mac):
    # break each string into 2-byte chunks of hexadecimal characters and store the result into the mac variable.
    mac = map('{:02x}'.format, mac)
    return ':'.join(mac).upper()


def ipv4_packet(ip_data):

    # The Protocol, Source and Destination address are included in the 8th, 12th and 16th octets.
    # IPv4 Addresses are 4 bytes long and the protocol is 2 bytes long
    # so now it is a matter of unpacking those values from the 20-byte long IP Packet.
    # 9x – Means 9 pad bytes of no value, we reach the 10th byte which holds the Protocol
    # B - means a byte string
    # 4s meaning a string of length 4 byte
    ip_protocol, source_ip, target_ip = unpack(
        '! 9x B 2x 4s 4s', ip_data[:20])
    return ip_protocol, ipv4(source_ip), ipv4(target_ip), ip_data[20:]


def ipv4(address):
    return '.'.join(map(str, address))


def udp_packet(ip_data):
    src_port, dst_port = unpack('! H H', ip_data[:4])
    return src_port, dst_port


main()
