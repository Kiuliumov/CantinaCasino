import os
from client import client
import dotenv
import discord

dotenv.load_dotenv()
token: str = os.getenv("TOKEN")

client.run(token)
