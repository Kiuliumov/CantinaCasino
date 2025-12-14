import random
import discord
from discord import app_commands
from discord.ext import commands
from src.DB import Database


SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = {
    "A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10
}


def draw_card():
    return random.choice(RANKS), random.choice(SUITS)


def hand_value(hand):
    value = sum(VALUES[r] for r, _ in hand)
    aces = sum(1 for r, _ in hand if r == "A")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def format_hand(hand):
    return " ".join(f"{r}{s}" for r, s in hand)


class BlackjackView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, db: Database):
        super().__init__(timeout=90)
        self.interaction = interaction
        self.db = db
        self.user_id = interaction.user.id
        self.reset_game()

    def reset_game(self):
        self.player_hand = [draw_card(), draw_card()]
        self.dealer_hand = [draw_card(), draw_card()]
        self.finished = False

        for item in self.children:
            item.disabled = False
        self.play_again.disabled = True

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.user_id

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.interaction.edit_original_response(view=self)

    def build_embed(self, reveal_dealer=False, footer=None):
        user = self.db.get_user(self.user_id)

        embed = discord.Embed(
            title="🎰 Blackjack",
            color=discord.Color.dark_gold()
        )

        embed.add_field(
            name="💰 Balance",
            value=f"{user.balance}",
            inline=False
        )

        embed.add_field(
            name="🧑 You",
            value=f"{format_hand(self.player_hand)}\n**Value:** {hand_value(self.player_hand)}",
            inline=False
        )

        if reveal_dealer:
            embed.add_field(
                name="🤖 Dealer",
                value=f"{format_hand(self.dealer_hand)}\n**Value:** {hand_value(self.dealer_hand)}",
                inline=False
            )
        else:
            r, s = self.dealer_hand[0]
            embed.add_field(
                name="🤖 Dealer",
                value=f"{r}{s} ❓",
                inline=False
            )

        if footer:
            embed.set_footer(text=footer)

        return embed

    async def end_game(self, interaction, result_text, payout):
        self.finished = True
        self.db.update_balance(self.user_id, payout)

        for item in self.children:
            item.disabled = True
        self.play_again.disabled = False

        await interaction.response.edit_message(
            embed=self.build_embed(reveal_dealer=True, footer=result_text),
            view=self
        )

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary, emoji="🃏")
    async def hit(self, interaction: discord.Interaction, _):
        self.player_hand.append(draw_card())

        if hand_value(self.player_hand) > 21:
            await self.end_game(interaction, "💥 You busted!", -10)
            return

        await interaction.response.edit_message(
            embed=self.build_embed(),
            view=self
        )

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary, emoji="✋")
    async def stand(self, interaction: discord.Interaction, _):
        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(draw_card())

        p, d = hand_value(self.player_hand), hand_value(self.dealer_hand)

        if d > 21 or p > d:
            await self.end_game(interaction, "🎉 You win!", 10)
        elif d > p:
            await self.end_game(interaction, "😞 Dealer wins.", -10)
        else:
            await self.end_game(interaction, "🤝 Push.", 0)

    @discord.ui.button(label="Double", style=discord.ButtonStyle.success, emoji="⏫")
    async def double(self, interaction: discord.Interaction, _):
        self.player_hand.append(draw_card())

        if hand_value(self.player_hand) > 21:
            await self.end_game(interaction, "💥 You busted on double!", -20)
            return

        while hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(draw_card())

        p, d = hand_value(self.player_hand), hand_value(self.dealer_hand)

        if d > 21 or p > d:
            await self.end_game(interaction, "🎉 You win (double)!", 20)
        elif d > p:
            await self.end_game(interaction, "😞 Dealer wins.", -20)
        else:
            await self.end_game(interaction, "🤝 Push.", 0)

    @discord.ui.button(label="Play Again", style=discord.ButtonStyle.primary, emoji="🔄", disabled=True)
    async def play_again(self, interaction: discord.Interaction, _):
        self.reset_game()
        await interaction.response.edit_message(
            embed=self.build_embed(),
            view=self
        )


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
