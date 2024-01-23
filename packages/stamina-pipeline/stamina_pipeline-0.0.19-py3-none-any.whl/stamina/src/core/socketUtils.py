from ..core.logging import log
from ..core.enums import messageTypes

import json
import socket

HEADER = 64
PORT = 5050
SERVER = "192.168.1.13"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg_type, msg_text={}):
    if not type(msg_text) == dict:
        raise TypeError('msg_text must be a dictionary')

    msg_text = json.dumps(msg_text)
    msg_dict = {
        'msg_type': msg_type.value,
        'msg_text': msg_text
    }
    msg_json = json.dumps(msg_dict)

    message = msg_json.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode()
    send_length += b' ' * (HEADER - len(send_length))  # send b -> byte repesentation of the string
    client.send(send_length)
    client.send(message)
    answer = client.recv(2048).decode(FORMAT)
    return answer


def disconnect():
    send(messageTypes.disconnect)
    log(f'Client Disconnected: {ADDR}')