import socket
import sys

ENCODING = 'ascii'


def start_client():
    # Check whether the inputs are enough to start the client or not
    if len(sys.argv) <= 3:
        print("Invalid input!")
        sys.exit()

    # Set the host address
    HOST = '127.0.0.1' if (sys.argv[1] == 'default') else sys.argv[1]
    # Set the port number
    PORT = 1370 if (sys.argv[2] == "default") else int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        if sys.argv[3] == "subscribe":
            subscribe(s, sys.argv)
        elif sys.argv[3] == "publish":
            publish(s, sys.argv)
        elif sys.argv[3] == "ping":
            send_message(s, "ping")
        else:
            print("Invalid input!")
            sys.exit()
        try:
            handler(s)
        except socket.error:
            print("Timeout. No response from server")
            sys.exit()


def handler(conn):
    # Time limit of 10 seconds
    conn.settimeout(10.0)
    while True:
        msg_len = int(conn.recv(1024).decode(ENCODING))
        msg = conn.recv(msg_len)
        if not msg:
            continue
        msg = msg.decode(ENCODING)
        conn.settimeout(None)
        split_msg = msg.split()
        if msg == "Topic not exists!":
            print(msg)
            sys.exit()
        elif split_msg[0] == "subACK":
            text = "Subscribing on "
            for msg in split_msg[1:]:
                text += " " + msg
            print(text)
        elif split_msg[0] == "pubACK":
            print("your message published successfully!")
            sys.exit()
        elif split_msg[0] == "ping":
            send_message(conn, "pong")
        elif split_msg[0] == "pong":
            print("pong received!")
            sys.exit()
        else:
            print(msg)


def subscribe(conn, message):
    if len(message[3:]) <= 1:
        print("No topic! Please try again.")
        sys.exit()
    msg = "subscribe"
    for message in message[4:]:
        msg += " " + message
    send_message(conn, msg)


def publish(conn, split_message):
    if len(split_message[4:]) <= 1:
        print("There is no topic or message!")
        sys.exit()
    message = "publish "
    for msg in split_message[4:]:
        message += msg + " "
    send_message(conn, message)


def send_message(conn, message):
    msg = message.encode(ENCODING)
    msg_len = str(len(msg)).encode(ENCODING)
    msg_len += b' ' * (1024 - len(msg_len))
    conn.send(msg_len)
    conn.send(msg)


if __name__ == '__main__':
    try:
        start_client()
    except socket.error:
        print("Cannot connect to server")
