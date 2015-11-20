import asyncio
import json

@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('0.0.0.0', 8000,
                                                        loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


class Socket(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def send(self, message):
        m = json.dumps(message) + "\n"
        self.loop.run_until_complete(tcp_echo_client(m, self.loop))

    def close(self):
        self.loop.close()

