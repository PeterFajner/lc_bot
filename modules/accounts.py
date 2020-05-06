from typing import List, Tuple

from superclasses import DiscordClient
import sqlite3

import discord
from tabulate import tabulate
from ranks import RANKS
import requests, lxml.html, cssselect


class Account:
    """
    Represents a linked Discord and Kattis user.
    """
    db_name = 'accounts.db'

    def __init__(self, discord_id: int, discord_name: str, kattis_name: str, score: float = 0, insert=True,
                 refresh=False):
        self._discord_id = discord_id
        self._discord_name = discord_name
        self._kattis_name = kattis_name
        self._score = score
        if insert:
            Account._exec('REPLACE INTO account VALUES (?, ?, ?, ?)', (discord_id, discord_name, kattis_name, score))
        if refresh:
            self.refresh()

    def __repr__(self):
        return str(self.__dict__)

    def refresh(self):
        """Fetch and update the user's Kattis score."""
        profile_url = 'https://open.kattis.com/users/{}'.format(self.kattis_name)
        # the xpath was determined manually through devtools, it might change in the future
        score_xpath = '/html/body/div[1]/div/div[1]/section/div/div/div[2]/div/table/tr[2]/td[2]'
        response = requests.get(profile_url)
        tree = lxml.html.fromstring(response.text)
        score_element = tree.xpath(score_xpath)[0]
        score = float(score_element.text)
        self.score = score

    @property
    def discord_id(self):
        return self._discord_id

    @property
    def discord_name(self):
        return self._discord_name

    @property
    def kattis_name(self):
        return self._kattis_name

    @kattis_name.setter
    def kattis_name(self, kattis_name):
        self._kattis_name = kattis_name
        Account._exec('UPDATE account SET kattis_name = ? WHERE discord_id = ?', (kattis_name, self.discord_id))

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score
        Account._exec('UPDATE account SET score = ? WHERE discord_id = ?', (score, self.discord_id))

    @property
    def rank(self):
        for rank in RANKS:
            if self.score >= rank[1]:
                return rank[0]

    @staticmethod
    def _connect() -> (sqlite3.Connection, sqlite3.Cursor):
        conn = sqlite3.connect(Account.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS account (discord_id INT PRIMARY KEY, discord_name TEXT UNIQUE, kattis_name TEXT, score REAL)')
        conn.commit()
        return conn, cursor

    @staticmethod
    def _exec(*query) -> List[Tuple[str or float]]:
        conn, cursor = Account._connect()
        cursor.execute(*query)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data

    @staticmethod
    def all() -> List['Account']:
        """Return all accounts."""
        result = Account._exec('SELECT discord_id, discord_name, kattis_name, score FROM account')
        return [Account(d[0], d[1], d[2], d[3], insert=False) for d in result]

    @staticmethod
    def filter(discord_id: int = None, discord_name: str = None, kattis_name: str = None) -> List['Account']:
        """Return accounts filtered by Discord username or Kattis username."""
        if discord_id:
            result = Account._exec(
                'SELECT discord_id, discord_name, kattis_name, score FROM account WHERE discord_id=?',
                discord_id)
        elif discord_name:
            result = Account._exec(
                'SELECT discord_id, discord_name, kattis_name, score FROM account WHERE discord_name=?',
                discord_name)
        elif kattis_name:
            result = Account._exec(
                'SELECT discord_id, discord_name, kattis_name, score FROM account WHERE kattis_name=?',
                kattis_name)
        else:
            raise ValueError('Must provide Discord id, Discord name, or Kattis name.')
        return [Account(d[0], d[1], d[2], d[3], insert=False) for d in result]

    @staticmethod
    def get(discord_id: int = None, discord_name: str = None, kattis_name: str = None) -> 'Account':
        """
        Return a single account, filtered by Discord username or Kattis username.

        :raise ValueError if there are multiple accounts or no accounts that match the filter.
        """
        result = Account.filter(discord_id=discord_id, discord_name=discord_name, kattis_name=kattis_name)
        if len(result) != 1:
            raise ValueError('{} results found', len(result))
        return result[0]


class AccountHandler(DiscordClient):
    async def on_ready(self):
        print('Account service enabled, logged on as {0}!'.format(self.user))

    # noinspection PyMethodMayBeStatic
    async def on_message(self, message: discord.Message):
        if message.content.startswith('/link'):
            try:
                command, kattis_name = message.content.split(' ')
            except ValueError:
                await message.channel.send('Usage: /link <your Kattis username>')
            else:
                account = Account(message.author.id, str(message.author), kattis_name, refresh=True)
                print('id', message.author.id)
                await message.channel.send(
                    'Linked {} to Kattis account **{}**, score: {}'.format(message.author.mention, kattis_name,
                                                                           account.score))
        elif message.content.startswith('/list'):
            accounts = Account.all()
            print('accounts', accounts)
            accounts_list = [(self.get_user(a.discord_id).display_name, a.kattis_name, a.score, a.rank) for a in
                             accounts]
            table = tabulate(accounts_list, headers=['User', 'Kattis Username', 'Score', 'Rank'], tablefmt='fancy_grid')
            await message.channel.send('```{}```'.format(table))
        elif message.content.startswith('/refresh'):
            try:
                account = Account.get(discord_id=message.author.id)
            except ValueError:
                await message.channel.send(
                    'No Kattis username linked for {}! Do `/link <kattis username>`'.format(message.author.mention))
            else:
                account.refresh()
                await message.channel.send(
                    'Kattis account {} linked to {} refreshed. Score: {}'.format(account.kattis_name,
                                                                                 message.author.mention, account.score))
        print('Message from {0.author}: {0.content}'.format(message))
