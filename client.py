import discord
from discord.ext import commands


# Instantiate a new discord client
client: commands.Bot = commands.Bot(

    command_prefix='!',
    case_insensitive=True,
    help_command=None,
    intents=discord.Intents.all()

)
