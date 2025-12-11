import discord
from discord import app_commands
from discord.ext import commands
import datetime
import os


class InfoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Join The Cantina",
            url="https://discord.com/invite/UEjnQeAHYx"
        ))
        self.add_item(discord.ui.Button(
            label="GitHub: CantinaCasino",
            url="https://github.com/Kiuliumov/CantinaCasino"
        ))


class InfoCog(commands.Cog):
    """Application info and development info for CantinaCasino."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.now()
        self.logo_path = os.path.join("images", "cantina-logo.png")
        if not os.path.exists(self.logo_path):
            self.logo_path = None

    @app_commands.command(name="info", description="Shows info about the CantinaCasino application")
    async def info(self, interaction: discord.Interaction):
        now = datetime.datetime.utcnow()
        uptime = now - self.start_time
        uptime_str = str(uptime).split(".")[0]

        embed = discord.Embed(
            title="🎰 CantinaCasino Application Info",
            color=discord.Color.blurple(),
            timestamp=now
        )

        embed.add_field(name="Project", value="CantinaCasino is a project by The Cantina", inline=False)
        embed.add_field(name="Application Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Application ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Total Users", value=len(set(self.bot.get_all_members())), inline=True)
        embed.add_field(name="Uptime", value=uptime_str, inline=False)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        view = InfoView()

        if self.logo_path:
            file = discord.File(self.logo_path, filename="cantina-logo.png")
            embed.set_image(url="attachment://cantina-logo.png")
            await interaction.response.send_message(embed=embed, file=file, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="about", description="General overview of CantinaCasino")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 About CantinaCasino",
            description=(
                "CantinaCasino is a custom-built gambling & progression application created by **The Cantina**.\n\n"
                "It features:\n"
                "🎲 Casino-style games\n"
                "💰 Global balances & leaderboards\n"
                "📈 Experience and leveling\n"
                "🛠️ Modular, scalable architecture\n\n"
                "CantinaCasino continues to expand with more games, systems, and features."
            ),
            color=discord.Color.gold()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        view = InfoView()

        if self.logo_path:
            file = discord.File(self.logo_path, filename="cantina-logo.png")
            embed.set_image(url="attachment://cantina-logo.png")
            await interaction.response.send_message(embed=embed, file=file, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="development", description="Shows information about The Cantina team")
    async def development(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛠️ About The Cantina",
            description=(
                "The Cantina is a self-run project with no outside financing.\n"
                "We aim to build the best chatbots and modern, responsive web applications.\n\n"
                "🤖 Custom Discord bots (Python + JavaScript)\n"
                "🌐 Web apps using React + Tailwind\n"
                "⚙️ Database work, APIs, automation\n"
                "🚀 Constantly learning new technologies\n\n"
                "Our goal: **Create the best chatbots in the market.**\n"
                "Interested in joining? Email: ikiuliumov@gmail.com"
            ),
            color=discord.Color.green()
        )

        view = InfoView()

        if self.logo_path:
            file = discord.File(self.logo_path, filename="cantina-logo.png")
            embed.set_thumbnail(url="attachment://cantina-logo.png")
            await interaction.response.send_message(embed=embed, file=file, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))
