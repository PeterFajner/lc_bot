from pathlib import Path
import sys
from discord.ext.commands import Bot, Command
import importlib

# add the filename of your module here
MODULES = [
    'accounts'
]

bot = Bot(command_prefix='!')


def main():
    global bot
    # get bot token
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
    # import bot extensions
    commands = []
    for module in MODULES:
        m = importlib.import_module('modules.' + module, '.')
        commands += [v for k,v in m.__dict__.items() if type(v) == Command]
    for command in commands:
        bot.add_command(command)
    # start bot
    bot.run(token)


if __name__ == '__main__':
    main()
