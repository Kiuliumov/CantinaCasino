from src.DB import Database
from functools import wraps
import discord

def autoregister(db: Database):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            db.add_user(interaction.user.id)
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
