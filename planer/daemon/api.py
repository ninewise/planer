
import asyncio
import json

from pony.orm import db_session, select
from pony.orm.serialization import json_converter
from simpledate import SimpleDate

from planer.daemon.db import db
from planer.config import config

__all__ = ["run_api_server"]


@asyncio.coroutine
def run_api_server():
    server_closing = asyncio.Future()
    coro = asyncio.start_server(ConnectionHandler(server_closing),
                                config['daemon']['host'],
                                config['daemon']['port'])
    server = yield from coro

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    message = yield from server_closing
    print(message)

    # Close the server
    server.close()
    yield from server.wait_closed()


class HandlerException(RuntimeError):
    pass


class ConnectionHandler(object):

    HANDLERS = {}

    def __init__(self, close_server):
        self.close_server = close_server
        self.handlers = self.__class__.HANDLERS
        self.handlers['exit'] = self.exit

    @asyncio.coroutine
    def __call__(self, reader, writer):

        data = yield from reader.readline()
        message = json.loads(data.decode())
        addr = writer.get_extra_info('peername')
        print("Received {} from {}".format(repr(message), addr))

        try:
            if "action" not in message:
                raise HandlerException("Please provide an action in your json.")
            action = message.pop("action", "no action")
            if action not in self.handlers:
                raise HandlerException(
                        "'{}' is not a valid action.".format(action))
            handler = self.handlers[action]
            answer = handler(message) or {}
            answer["success"] = True
        except HandlerException as e:
            answer = dict(error=str(e), success=False)
        writer.write(json.dumps(answer, default=json_converter).encode())
        yield from writer.drain()

        print("Close the client socket")
        writer.close()

    def exit(self, message):
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


@ConnectionHandler.add_handler_for("help")
def help(_):
    return dict(commands=list(ConnectionHandler.HANDLERS.keys()))


@ConnectionHandler.add_handler_for("list calendars")
@db_session
def list_calendars(_):
    return dict(ids=list(select(c.id for c in db.Calendar)))


@db_session
def get_entity(id, table):
    if not id: raise HandlerException("Please provide an id.")
    with db_session: entity = table.get(id=id)
    if not entity:
        raise HandlerException(
                "{} with that id not found.".format(table._table_))
    return entity


@ConnectionHandler.add_handler_for("show calendar")
def show_calendar(message):
    calendar = get_entity(message.get("id", None), db.Calendar)
    return calendar.to_dict()


@ConnectionHandler.add_handler_for("list calendar events")
def list_calendar_events(message):
    calendar = get_entity(message.get("id", None), db.Calendar)
    with db_session:
        events = list(select(e.id for e in db.Event if e.calendar == calendar))
    return dict(ids=events)


@ConnectionHandler.add_handler_for("show event")
@db_session # TODO remove this when somehow to_dict no longer
            # retrieves the calendar
def show_event(message):
    event = get_entity(message.get("id", None), db.Event)
    return event.to_dict()


@ConnectionHandler.add_handler_for("new event")
def new_event(message):
    try:
        with db_session:
            calendar = get_entity(message.get("calendar", None), db.Calendar)
            event = dict(calendar=calendar,
                         summary=message["summary"],
                         description=message.get("description", None),
                         location=message.get("location", ""))
            timezone = message.get('timezone', config['remote']['timezone'])
            event["start_time"] = SimpleDate(message["start_time"], tz=timezone).datetime
            event["end_time"] = SimpleDate(message["end_time"], tz=timezone).datetime
            e = db.Event(**event)
        return dict(id=e.id)
    except Exception as exc:
        raise HandlerException(exc)


