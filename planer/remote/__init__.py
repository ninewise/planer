
import argparse
import asyncio
import json
import pprint

from planer.config import config


# let's create some subparsers for the subcommands
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


parser_exit = subparsers.add_parser("exit")
parser_exit.set_defaults(action="exit")


parser_echo = subparsers.add_parser("echo")
parser_echo.set_defaults(action="echo")


parser_list_calendars = subparsers.add_parser("list")
parser_list_calendars.set_defaults(action="list calendars")


parser_calendar = subparsers.add_parser("calendar")
parser_calendar.add_argument("id", type=int)
calendar_subparsers = parser_calendar.add_subparsers()

parser_calender_show = calendar_subparsers.add_parser("show")
parser_calender_show.set_defaults(action="show calendar")

parser_calendar_list_events = calendar_subparsers.add_parser("list")
parser_calendar_list_events.set_defaults(
        action="list calendar events")

parser_calendar_new_event = calendar_subparsers.add_parser("new-event")
parser_calendar_new_event.set_defaults(action="new event")
parser_calendar_new_event.add_argument("summary")
parser_calendar_new_event.add_argument("start_time")
parser_calendar_new_event.add_argument("end_time")
parser_calendar_new_event.add_argument("--description")
parser_calendar_new_event.add_argument("--location")
parser_calendar_new_event.add_argument("--timezone")


parser_event = subparsers.add_parser("event")
parser_event.add_argument("id", type=int)
event_subparsers = parser_event.add_subparsers()

parser_event_show = event_subparsers.add_parser("show")
parser_event_show.set_defaults(action="show event")


async def send(loop, message):
    "Send the keyword arguments as a JSON to the server."
    reader, writer = await asyncio.open_connection(
            config['daemon']['host'],
            config['daemon']['port'],
            loop=loop)

    writer.write("{}\n".format(json.dumps(message)).encode())
    await writer.drain()
    received = await reader.readline()
    writer.close()

    return json.loads(received.decode())

def main():
    namespace = parser.parse_args()

    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(send(loop, vars(namespace)))
    loop.close()

    pprint.pprint(answer)






