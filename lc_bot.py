import argparse
import asyncio
from threading import Thread
from pathlib import Path

# noinspection PyUnresolvedReferences
from modules import *
from superclasses import DiscordClient, ScheduledTask
import sys


def main():
    # authenticate with Discord
    token = None
    try:
        with open('token.txt') as f:
            token = f.read()
    except FileNotFoundError:
        Path('token.txt').touch()
    finally:
        if not token:
            print('Error: Put a Discord token in token.txt', file=sys.stderr)
            return
    # parse args and run task
    parser = argparse.ArgumentParser(description='Run scheduled task.')
    parser.add_argument('task', type=str, nargs='?', default='run',
                        help='Name of the task to run')
    parser.add_argument('parameters', type=str, nargs='*', help='Parameters to the task')
    args = parser.parse_args()
    if args.task == 'run':
        loop = asyncio.get_event_loop()
        for Client in DiscordClient.__subclasses__():
            loop.create_task(Client().start(token))
        loop.run_forever()
    else:
        tasks = ScheduledTask.__subclasses__()
        for Task in tasks:
            if Task.name() == args.task:
                Task.exec(*args.parameters)

if __name__ == '__main__':
    main()
