from superclasses import DiscordClient
import sqlite3

import discord


class AccountService:
    def __init__(self):
        self.db_name = 'accounts.db'

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS account (discord_name TEXT PRIMARY KEY, kattis_name TEXT, score REAL)')
        conn.commit()
        return conn, c

    def exec(self, *query) -> sqlite3.Connection:
        conn, c = self.connect()
        c.execute(*query)
        data = c.fetchall()
        conn.commit()
        conn.close()
        return data

    def register(self, discord_name, kattis_name, score=0):
        self.exec('INSERT INTO account VALUES (?, ?, ?)', (discord_name, kattis_name, score))

    def get_all(self):
        data = self.exec('SELECT * FROM account')
        print('data', data)
        return data



class AccountHandler(DiscordClient):
    async def on_ready(self):
        print('Account service enabled, logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.content.startswith('/register'):
            try:
                _, kattis_name = message.content.split(' ')
            except ValueError:
                await message.channel.send('Usage: /register <your Kattis username>')
            else:
                AccountService().register(str(message.author), kattis_name)
                points = 0
                await message.channel.send(
                    'Registered {} as **{}** on Kattis, points: {}'.format(message.author.mention, kattis_name, points))
        elif message.content.startswith('/list'):
            AccountService().get_all()


        print('Message from {0.author}: {0.content}'.format(message))
