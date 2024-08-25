import asyncio
import logging
import random

HOST = '127.0.0.1'
PORT = 8888
TIMEOUT_START = 5
TIMEOUT_END = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


async def client(client_id):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    for i in range(5):
        message = f'Сообщение {i + 1} от ID {client_id}'
        logging.info(f'ID {client_id}: отправка сообщения: {message}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        logging.info(f'ID {client_id}: получено сообщение: {data.decode()}')

        await asyncio.sleep(random.randint(TIMEOUT_START, TIMEOUT_END))

    writer.close()
    await writer.wait_closed()
    logging.info(f'ID {client_id} - соединение закрыто')


async def main():
    clients = [client(i) for i in range(10)]
    await asyncio.gather(*clients)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.info(f'Ошибка работы с сервером {e}')
