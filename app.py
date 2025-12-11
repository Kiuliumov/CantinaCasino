import os
from client import client
import dotenv

dotenv.load_dotenv()

token: str = os.getenv('TOKEN')

loaded_commands = []

@client.event
async def setup_hook():
    global loaded_commands
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            await client.load_extension(cog_name)
            print(f"Loaded extension: {filename}")
            cog = client.get_cog(filename[:-3])
            if cog:
                for command in cog.get_commands():
                    loaded_commands.append(command.name)

@client.event
async def on_ready():
    print("==============================")
    print("🎰 Cantina Casino Bot is Online! 🎰")
    print(f"Application name: {client.user.name}")
    print(f"Application ID   : {client.user.id}")
    print(f"Servers  : {len(client.guilds)}")
    if loaded_commands:
        print(f"Loaded Commands: {', '.join(loaded_commands)}")
    print("==============================")

client.run(token)
