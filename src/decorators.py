from database_serivce import DatabaseService
from functools import wraps
import discord


def auto_register(db: DatabaseService):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            db.add_user(interaction.user.id)
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator
