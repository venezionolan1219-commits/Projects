import socket

HOST, PORT, BUFSIZE = 'localhost', 5050, 4096
client = socket.socket()
client.connect((HOST, PORT))


def receive():
    try:
        return client.recv(BUFSIZE).decode().strip()
    except ConnectionResetError:
        print("Server disconnected unexpectedly.")
        return None


def send(data):
    client.send(str(data).encode().strip())


try:
    print(receive())
    send(input())
    print(receive())
    send(input())

    while True:
        reply = receive()
        if reply is None:
            break
        print(reply)
        branch = input().strip()
        send(branch)
        if branch == '':
            break
finally:
    client.close()
