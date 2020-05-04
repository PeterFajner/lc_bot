import discord
from abc import ABC, abstractmethod


class ScheduledTask(ABC):
    @staticmethod
    @abstractmethod
    def name():
        """
        The name of this scheduled task.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def exec():
        """
        The task to execute.
        """
        raise NotImplementedError()


class DiscordClient(discord.Client):
    """
    Transparent superclass to gather all client modules.
    """
    pass