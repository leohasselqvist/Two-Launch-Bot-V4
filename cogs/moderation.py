from discord.ext import commands
from discord import Embed
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="clear",
        description="Clear a specified number of messages",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="amount",
                description="How many messages to clear",
                option_type=SlashCommandOptionType.INTEGER,
                required=True,
            )
        ])
    async def clear(self, ctx: SlashContext, amount: int):
        await ctx.send(f"Cleared {amount} messages!")


def setup(client):
    client.add_cog(Moderation(client))
