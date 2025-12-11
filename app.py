import os
from client import client
import dotenv

dotenv.load_dotenv()

token: str = os.getenv('TOKEN')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print(f"==============================")
    print(f"🎰 Cantina Casino Bot is Online! 🎰")
    print(f"Application name: {client.user.name}")
    print(f"Application ID   : {client.user.id}")
    print(f"Servers  : {len(client.guilds)}")
    print(f"==============================")

client.run(token)