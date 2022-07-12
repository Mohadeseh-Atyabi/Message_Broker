import socket
import threading

HOST = '127.0.0.1'
PORT = 1370
ENCODING = 'ascii'

client_topic = {}  # It's like {"topic": "client"}


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Server starts listening ...")
    while True:
        conn, address = s.accept()
        t = threading.Thread(target=handler, args=(conn, address))
        t.start()


def handler(conn, address):
    print("New connection from ", address)
    while True:
        try:
            msg_len = int(conn.recv(1024).decode(ENCODING))
            msg = conn.recv(msg_len)
            if not msg:
                continue
            msg = msg.decode(ENCODING)
            print("Message received is: ", msg)
            split_msg = msg.split()
            if split_msg[0] == 'subscribe':
                subscribe(conn, split_msg)
            elif split_msg[0] == 'publish':
                publish(conn, split_msg)
            elif split_msg[0] == 'ping':
                print("Sending pong")
                send_message(conn, "pong")
            elif split_msg[0] == 'pong':
                send_message(conn, "ping")
        except:
            disconnect_client(conn)
            print("Disconnected by ", address)
            break
    conn.close()


def subscribe(conn, split_message):
    for message in split_message[1:]:
        if message in client_topic.keys():
            if conn not in client_topic[message]:
                client_topic[message].append(conn)
        else:
            client_topic[message] = [conn]

    message = "subACK"
    for topic in client_topic.keys():
        if conn in client_topic[topic]:
            message += " " + topic
    send_message(conn, message)


def publish(conn, split_message):
    message = split_message[1] + ":"
    for msg in split_message[2:]:
        message += " " + msg
    if split_message[1] in client_topic.keys():
        send_message(conn, "pubACK")
        for client in client_topic[split_message[1]]:
            try:
                send_message(client, message)
            except:
                disconnect_client(client)
    else:
        send_message(conn, "Topic not exists!")


def disconnect_client(conn):
    changed = False
    temp = False
    for topic in client_topic:
        if conn in client_topic[topic]:
            temp = topic
            changed = True
            client_topic[topic].remove(conn)
    conn.close()
    if changed and len(client_topic[temp]) == 0:
        client_topic.pop(temp, None)


def send_message(conn, message):
    msg = message.encode(ENCODING)
    msg_len = str(len(msg)).encode(ENCODING)
    msg_len += b' ' * (1024 - len(msg_len))
    conn.send(msg_len)
    conn.send(msg)


if __name__ == '__main__':
    start_server()
