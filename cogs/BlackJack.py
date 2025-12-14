import random
import discord
from discord import app_commands
from discord.ext import commands
from src.DB import Database


class BlackjackCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="blackjack", description="Play blackjack")
    async def blackjack(self, interaction: discord.Interaction):
        self.db.add_user(interaction.user.id)

        view = BlackjackView(interaction, self.db)

        await interaction.response.send_message(
            embed=view.build_embed(),
            view=view
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(BlackjackCog(bot))
