import discord
from discord.ext import commands
from discord import Role, Guild
from datetime import datetime
from main import bot

    
def is_ta(message) -> bool:
    """check if who sent a message is a TA, 
    userful for purge messages as only TA's should be able to purge """
    return "LC Staff" in [x.name for x in message.author.roles]


@commands.command()
async def url(ctx):
    await ctx.send("https://github.com/PeterFajner/lc_bot")


@commands.command()
async def delete(ctx, args):
    """called as !delete, deletes messages in a channel, 
        arguements:
        - !delete all: deletes all messages in a channel (50)
        - !delete num: deletes num messages in a channel (WIP)
            
    """
    await ctx.send("Delete function called")
    if args == "all":
        await ctx.channel.purge(limit=50)
    elif int(args):
        args = int(args)
        deleted = await ctx.channel.purge(limit=args)
        await ctx.send("Deleted {} message(s)".format(len(deleted)))
    else:
        await ctx.send("Execption: Sorry I take 'all' or numbers")


@commands.command()
async def active(ctx):
    """active function, called by !active 
    This function gives the ON DUTY role to a user which calls it 
    with the permissions to have it, the is_ta function checks that
    the user actually has the "LC staff role"
    """
    on_duty = ctx.guild.get_role(role_id=689482996356612166)
    if is_ta(ctx):
        await ctx.send("you work here dude, ill give you a role now")
        await ctx.author.add_roles(on_duty)
        await ctx.send("I have given you the @ON DUTY role")
    else:
        await ctx.send("Hi, you do not work here")


@commands.command()
async def unactive(ctx):
    """Opposite of active"""
    on_duty = ctx.guild.get_role(role_id=689482996356612166)
    if is_ta(ctx):
        await ctx.send("Nice work dude,taking your role away")
        await ctx.author.remove_roles(on_duty)
        await ctx.send("I have taken your role away, Ganbate")
    else:
        await ctx.send("Hi, you do not work here")


@commands.command()
async def embed(ctx):
    # https://discohook.org/
    embed = discord.Embed()
    embed.title = "Learning Centre Discord Server"
    embed.url = "https://learning.cs.dal.ca"
    embed.description = "This is an embedded message"
    embed.set_author(name="Victor Popoola", url="https://victorXLR.me")
    embed.color(discord.Color.orange())

    await ctx.send(embed=embed)


@commands.command()
async def special(ctx):
    embed = discord.Embed(
        title="Learning Centre Discord Server",
        description="""
        Discohook is a free tool that allows you to build 
        Discord messages and embeds for use in your server.""",
        color=0x000000,
    )
    embed.url = "https://learning.cs.dal.ca"
    embed.set_author(name="Victor Popoola", url="http://google.com")
    embed.add_field(name="Monday", value="Pain")
    embed.add_field(name="Tuesday", value="Pain")
    embed.add_field(name="Wednesday", value="Pain")
    embed.add_field(name="Thurday", value="Pain")
    embed.add_field(name="Friday", value="Pain")
    embed.add_field(name="Saturday", value="Pain")
    await ctx.send(embed=embed)
