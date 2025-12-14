import os
from client import client
import dotenv
import discord

dotenv.load_dotenv()
token: str = os.getenv('TOKEN')

@client.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            await client.load_extension(cog_name)
            print(f"Loaded extension: {filename}")

@client.event
async def on_ready():
    try:
        GUILD_ID = 776155094868819999
        guild = discord.Object(id=GUILD_ID)
        synced_commands = await client.tree.sync(guild=guild)
        synced_names = [cmd.name for cmd in synced_commands]
    except Exception as e:
        print(f"Failed to sync commands: {e}")
        synced_names = []

    print("==============================")
    print("🎰 Cantina Casino Bot is Online! 🎰")
    print(f"Application name: {client.user.name}")
    print(f"Application ID   : {client.user.id}")
    print(f"Servers          : {len(client.guilds)}")
    print(f"Users: {len(client.users)}")
    if synced_names:
        print(f"Synced Commands  : {', '.join(synced_names)}")
    print("==============================")

client.run(token)
