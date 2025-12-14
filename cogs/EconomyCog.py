import discord
from discord import app_commands
from discord.ext import commands
import datetime
from typing import List
from src.DB import Database, User
from src.decorators import autoregister

class LeaderboardView(discord.ui.View):
    def __init__(self, users: List[User], title: str, per_page: int = 10):
        super().__init__(timeout=120)
        self.users = users
        self.title = title
        self.per_page = per_page
        self.current_page = 0
        self.max_page = (len(users) - 1) // per_page

        self.update_buttons()

    def update_buttons(self):
        for child in self.children:
            if child.custom_id == "previous":
                child.disabled = self.current_page == 0
            elif child.custom_id == "next":
                child.disabled = self.current_page == self.max_page

    def get_page_embed(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page_users = self.users[start:end]

        description = ""
        for i, u in enumerate(page_users, start=start+1):
            if "Balance" in self.title:
                description += f"**{i}.** <@{u.discord_id}> — {u.balance:,} coins (Level {u.level}, XP {u.experience:,})\n"
            else:
                description += f"**{i}.** <@{u.discord_id}> — {u.experience:,} XP (Level {u.level}, {u.balance:,} coins)\n"

        embed = discord.Embed(
            title=self.title,
            description=description or "No users yet",
            color=discord.Color.gold() if "Balance" in self.title else discord.Color.green()
        )
        embed.set_footer(text=f"Page {self.current_page + 1}/{self.max_page + 1}")
        return embed

    @discord.ui.button(emoji="<:arrowleft:1210243998384652308>", style=discord.ButtonStyle.primary, custom_id="previous")
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(emoji="<:arrowright:1210243999982682173>", style=discord.ButtonStyle.primary, custom_id="next")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)


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
    async def baltop(self, interaction: discord.Interaction):
        limit = 10
        top_users: List[User] = self.db.top_balance(limit=limit)
        view = LeaderboardView(top_users, title="Balance Leaderboard", per_page=10)
        await interaction.response.send_message(embed=view.get_page_embed(), view=view)

    @app_commands.command(name="xptop", description="Show top users by experience")
    @autoregister(db=Database("sqlite:///casino.db"))
    async def xptop(self, interaction: discord.Interaction):
        limit = 10
        top_users: List[User] = self.db.top_experience(limit=limit)
        view = LeaderboardView(top_users, title="Experience Leaderboard", per_page=10)
        await interaction.response.send_message(embed=view.get_page_embed(), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(EconomyCog(bot))
