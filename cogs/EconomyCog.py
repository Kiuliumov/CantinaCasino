import discord
from discord import app_commands
from discord.ext import commands
import datetime
from typing import List
from src.DB import Database, User
from src.decorators import autoregister

class EconomyCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db_path: str = "sqlite:///casino.db"):
        self.bot = bot
        self.db = Database(db_path)
        self.daily_cooldowns = {}
        self.weekly_cooldowns = {}

    @app_commands.command(name="balance", description="Check your balance, level and XP")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def balance(self, interaction: discord.Interaction):
        user = self.db.get_user(interaction.user.id)
        embed = discord.Embed(
            title=f"💰 {interaction.user.name}'s Balance",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Coins", value=f"{user.balance:,}", inline=True)
        embed.add_field(name="Level", value=f"{user.level}", inline=True)
        embed.add_field(name="XP", value=f"{user.experience:,}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily 1,000 coins and 10 XP")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def daily(self, interaction: discord.Interaction):
        now = datetime.datetime.utcnow()
        user = self.db.get_user(interaction.user.id)
        last = self.daily_cooldowns.get(interaction.user.id)

        if last and (now - last).total_seconds() < 24*3600:
            remaining = 24*3600 - (now - last).total_seconds()
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            await interaction.response.send_message(f"⏳ You can claim your daily reward in {hours}h {minutes}m.")
            return

        self.daily_cooldowns[interaction.user.id] = now
        self.db.update_balance(interaction.user.id, 1000)
        self.db.update_experience(interaction.user.id, 10)
        user = self.db.get_user(interaction.user.id)

        embed = discord.Embed(
            title="✅ Daily Reward Claimed!",
            description="You received **1,000 coins** and **10 XP**.",
            color=discord.Color.gold(),
            timestamp=now
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="New Balance", value=f"{user.balance:,} coins", inline=True)
        embed.add_field(name="Level", value=f"{user.level}", inline=True)
        embed.add_field(name="XP", value=f"{user.experience:,}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="weekly", description="Claim your weekly 50,000 coins and 50 XP")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def weekly(self, interaction: discord.Interaction):
        now = datetime.datetime.utcnow()
        user = self.db.get_user(interaction.user.id)
        last = self.weekly_cooldowns.get(interaction.user.id)

        if last and (now - last).total_seconds() < 7*24*3600:
            remaining = 7*24*3600 - (now - last).total_seconds()
            days = int(remaining // (24*3600))
            hours = int((remaining % (24*3600)) // 3600)
            await interaction.response.send_message(f"⏳ You can claim your weekly reward in {days}d {hours}h.")
            return

        self.weekly_cooldowns[interaction.user.id] = now
        self.db.update_balance(interaction.user.id, 50000)
        self.db.update_experience(interaction.user.id, 50)
        user = self.db.get_user(interaction.user.id)

        embed = discord.Embed(
            title="🏆 Weekly Reward Claimed!",
            description="You received **50,000 coins** and **50 XP**.",
            color=discord.Color.green(),
            timestamp=now
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="New Balance", value=f"{user.balance:,} coins", inline=True)
        embed.add_field(name="Level", value=f"{user.level}", inline=True)
        embed.add_field(name="XP", value=f"{user.experience:,}", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="baltop", description="Show top users by balance")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def baltop(self, interaction: discord.Interaction, limit: int = 10, offset: int = 0):
        top_users: List[User] = self.db.top_balance(limit=limit, offset=offset)
        description = ""
        for i, u in enumerate(top_users):
            description += f"**{i+1+offset}.** <@{u.discord_id}> — {u.balance:,} coins (Level {u.level}, XP {u.experience:,})\n"
        embed = discord.Embed(title="💰 Balance Leaderboard", description=description or "No users yet", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="xptop", description="Show top users by experience")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def xptop(self, interaction: discord.Interaction, limit: int = 10, offset: int = 0):
        top_users: List[User] = self.db.top_experience(limit=limit, offset=offset)
        description = ""
        for i, u in enumerate(top_users):
            description += f"**{i+1+offset}.** <@{u.discord_id}> — {u.experience:,} XP (Level {u.level}, {u.balance:,} coins)\n"
        embed = discord.Embed(title="🧩 Experience Leaderboard", description=description or "No users yet", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(EconomyCog(bot))
