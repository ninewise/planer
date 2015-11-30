
import argparse
import asyncio
import json
import pprint

from planer.config import config


# let's create some subparsers for the subcommands
parser = argparse.ArgumentParser(description="""
        Used for command line remote access to the planer daemon. This
        means the program will horribly fail when the daemon is
        unreachable.

        The `start_time` and `end_time` arguments are in ISO datetime
        format, as detailed on https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations
        (but lacking a timezone). The `duration` is passed in ISO
        duration format PnYnMnDTnHnMnS, the first mentioned on
        https://en.wikipedia.org/wiki/ISO_8601#Durations. Finally, the
        timezone is given like "Europe/Brussels".
        """)
parser.add_argument("action")
parser.add_argument("-c", "--calendar", type=int)
parser.add_argument("-s", "--summary")
parser.add_argument("-S", "--start-time")
parser.add_argument("-E", "--end-time")
parser.add_argument("-D", "--duration", help="The duration in H*:M*:S*")
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


