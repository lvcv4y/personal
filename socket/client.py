import socket
import threading

"""
Little UDP chatting client. Connect to "server.py" to chat with other clients.
Note: be careful to correctly set the server's ip and port, and not to set an already-in-use port.
"""

SERVER = ('localhost', 1234)  # (ip, port)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
user = input('name>')
port = int(input('port>'))
s.bind(('localhost', port))


def receiving_process():
    while 1:
        global user
        data = s.recvfrom(1024)[0]
        data = data.decode('utf-8')
        if data[:3] == 'new':
            print('{} nous a rejoint'.format(data[4:]))
        elif data[:3] == 'dis':
            print('{} est parti'.format(data[4:]))
        else:
            data = data.split(':')
            if data[0] != user:
                print('<{}> : {}'.format(data[0], data[1]))


thr = threading.Thread(target=receiving_process)
thr.daemon = True
thr.start()

s.sendto('new {}'.format(user).encode('utf8'), SERVER)

while 1:
    msg = input('')
    if msg == 'disconnect':
        s.sendto(('dis ' + user).encode('utf8'), SERVER)
        s.close()
        break
    msg = "{}:{}".format(user, msg)
    s.sendto(msg.encode('utf8'), SERVER)


