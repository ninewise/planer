
import argparse
import asyncio
import json
import pprint

from planer.config import config


# let's create some subparsers for the subcommands
parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("-c", "--calendar", type=int)
parser.add_argument("-s", "--summary")
parser.add_argument("-S", "--start-time")
parser.add_argument("-E", "--end-time")
parser.add_argument("-d", "--description")
parser.add_argument("-l", "--location")
parser.add_argument("-z", "--timezone")
parser.add_argument("-e", "--event", type=int)


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


def clean_args(args):
    return { key: value for key, value in vars(args).items() if value is not None }


def main():
    namespace = parser.parse_args()

    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(send(loop, clean_args(namespace)))
    loop.close()

    pprint.pprint(answer)


