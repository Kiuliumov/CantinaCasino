import discord
from discord import app_commands
from discord.ext import commands
import datetime
import os

class InfoCog(commands.Cog):
    """Application info and development info for CantinaCasino."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
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

        if self.logo_path:
            file = discord.File(self.logo_path, filename="cantina-logo.png")
            embed.set_image(url="attachment://cantina-logo.png")
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="development", description="Shows information about The Cantina team")
    async def development(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛠️ About The Cantina",
            description=(
                "The Cantina is a self-run project with no outside financing.\n"
                "Our mission is to create the best chatbots in the market while building modern, responsive web applications.\n\n"
                "🤖 Experienced in building custom Discord bots with JavaScript and Python\n"
                "🌐 Skilled at creating modern, responsive web apps using React and Tailwind\n"
                "⚙️ Integrating APIs, handling databases, and automating tasks\n"
                "🚀 Always learning new frameworks and best practices in full-stack development\n\n"
                "Our goal is to create the best chatbots in the market.\n"
                "If you want to join us: ikiuliumov@gmail.com"
            ),
            color=discord.Color.green()
        )

        if self.logo_path:
            file = discord.File(self.logo_path, filename="cantina-logo.png")
            embed.set_thumbnail(url="attachment://cantina-logo.png")
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))
