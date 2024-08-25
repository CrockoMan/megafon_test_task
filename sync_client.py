import logging
import random
import socket
import time

HOST = '127.0.0.1'
PORT = 8888
TIMEOUT_START = 5
TIMEOUT_END = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def tcp_client(client_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        for i in range(5):
            message = f'Сообщение {i + 1} от ID {client_id}'
            logging.info(f'ID {client_id}: отправка сообщения: {message}')
            client_socket.sendall(message.encode())

            data = client_socket.recv(1024)
            logging.info(f'ID {client_id}: получено сообщение: {data.decode()}')

            time.sleep(random.randint(TIMEOUT_START, TIMEOUT_END))


if __name__ == '__main__':
    for i in range(10):
        tcp_client(i)
