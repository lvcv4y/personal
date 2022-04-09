import socket
import threading

"""
Little UDP chatting server. It allows multiple connections at once.
"""

PORT = 1234

client = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", PORT))
print("[*] Server is running...")

while 1:
    try:
        data, addr = s.recvfrom(1024)
    except IOError as e:
        print(e)
        continue

    print('[*] data received from {} : "{}"'.format(addr, data))
    if addr not in client:
        client.append(addr)
        for c in client:
            s.sendto(data, c)
    else:
        if data.decode('utf-8')[:3] == 'dis':
            for c in client:
                s.sendto("dis {}".format(data.decode('utf-8')[4:]).encode('utf-8'), c)
            client.remove(addr)
        else:
            for c in client:
                s.sendto(data, c)
