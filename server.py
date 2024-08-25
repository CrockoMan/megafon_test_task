import asyncio

HOST = '127.0.0.1'
PORT = 8888


class Server(asyncio.Protocol):
    active_clients = 0
    shutdown_event = asyncio.Event()

    def connection_made(self, transport):
        self.transport = transport
        Server.active_clients += 1
        print(f'Клиент подключен. Клиентов: {Server.active_clients}')

    def data_received(self, data):
        print(f'Входящее сообщение: {data.decode()}')
        self.transport.write(data)
        print(f'Ответ: {data.decode()}')

    def connection_lost(self, exc):
        Server.active_clients -= 1
        print(f'Клиент отключен. Клиентов: {Server.active_clients}')
        if Server.active_clients == 0:
            self.shutdown_event.set()


async def run_server():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(Server, HOST, PORT)
    print(f'Сервер запущен.  {HOST}:{PORT}')
    async with server:
        await Server.shutdown_event.wait()
    print('Сервер остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print('Сервер принудительно остновлен')
