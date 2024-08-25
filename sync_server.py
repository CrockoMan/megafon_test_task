import socket
import time
import sqlite3

HOST = '127.0.0.1'
PORT = 8888
STOP_SERVER_TIMEOUT = 20
DB_NAME = 'requests.db'


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f'Сервер запущен. {host}:{port}')
        self.create_db()

    def create_db(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        self.cursor.execute('DELETE FROM requests')
        self.conn.commit()

    def log_request(self, request_text):
        self.cursor.execute(
            'INSERT INTO requests (request_text) VALUES (?)',
            (request_text,)
        )
        self.conn.commit()

    def handle_client(self, client_socket):
        with client_socket:
            print('Клиент подключен.')
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                request_text = data.decode()
                print(f'Входящее сообщение: {request_text}')
                self.log_request(request_text)
                client_socket.sendall(data)
                print(f'Ответ: {request_text}')
            print('Клиент отключен.')

    def start(self):
        last_client_time = time.time()

        try:
            while True:
                if time.time() - last_client_time > STOP_SERVER_TIMEOUT:
                    print(f'Нет подключений в течении {STOP_SERVER_TIMEOUT} '
                          'секунд. Остановка работы сервера.')
                    break
                self.server_socket.settimeout(1.0)
                try:
                    client_socket, addr = self.server_socket.accept()
                    last_client_time = time.time()
                    self.handle_client(client_socket)
                except socket.timeout:
                    continue

        except KeyboardInterrupt:
            print('Сервер принудительно остановлен')
        finally:
            self.server_socket.close()
            self.conn.close()
            print('Сокет закрыт')


if __name__ == '__main__':
    server = Server()
    server.start()
