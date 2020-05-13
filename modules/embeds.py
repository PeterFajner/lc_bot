# This module contains commands for dealing with Embedded Messages
import discord
from discord.ext import commands
from discord import Role, Guild
from datetime import datetime
from main import bot


@commands.command()
async def template(ctx):
    """get a template of normal messages in the channel"""
    e_message = discord.Embed(
        title="Getting Help",
        description="""
    In other to get help from any of a TA's contact them by mentioning the 
    <@&689482996356612166>  role in the <#689489210150748207> channel. 

    - Ensure your username/nickname is your real name 

    > <@&689482996356612166>  Need help with CSCI 3130

    After a TA has helped you, your message will be deleted by the TA
    """,
        color=0x15793D,
    )
    await ctx.send(embed=e_message)


