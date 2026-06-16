from client import Client


@client.event
async def on_ready():
    try:
        synced_commands = await client.tree.sync()
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
