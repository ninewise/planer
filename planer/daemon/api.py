
import asyncio
import json

#from pony.orm import db_session, select
#from simpledate import SimpleDate

#from planer.daemon.db import db
#from planer.daemon.json_converter import as_json
from planer.config import config

__all__ = ["run_api_server"]


def run_api_server():
    loop = asyncio.get_event_loop()
    server_closing = asyncio.Future()
    coro = asyncio.start_server(ConnectionHandler(server_closing),
                                config['daemon']['host'],
                                config['daemon']['port'],
                                loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    message = loop.run_until_complete(server_closing)
    print(message)

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ConnectionHandler(object):

    HANDLERS = {}

    def __init__(self, close_server):
        self.close_server = close_server
        self.handlers = self.__class__.HANDLERS
        self.handlers['close'] = self.close

    @asyncio.coroutine
    def __call__(self, reader, writer):

        data = yield from reader.readline()
        message = json.loads(data.decode())
        addr = writer.get_extra_info('peername')
        print("Received {} from {}".format(repr(message), addr))

        if message == "close":
            self.close_server.set_result("Closing the server on request")
            writer.close()
            return

        action = message.pop("action", "no action")
        handler = self.handlers.get(action, None) or (lambda _: dict(
                message="'{}' is not a valid action.".format(action)))
        answer = handler(message) or dict(message="OK")
        writer.write(json.dumps(answer).encode())
        yield from writer.drain()

        print("Close the client socket")
        writer.close()

    def close(self, message):
        self.close_server.set_result("Closing server on request.")

    @classmethod
    def add_handler_for(cls, action):
        def handler_adder(handler):
            cls.HANDLERS[action] = handler
            return handler
        return handler_adder


@ConnectionHandler.add_handler_for("echo")
def echo(message):
    message["action"] = "echo"
    return message

@ConnectionHandler.add_handler_for("no action")
def no_action(message):
    return dict(message="Please supply an action (e.g. 'help') in your json.")

@ConnectionHandler.add_handler_for("help")
def help(message):
    return dict(commands=list(ConnectionHandler.HANDLERS.keys()))


