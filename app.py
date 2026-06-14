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


client.run(token)
