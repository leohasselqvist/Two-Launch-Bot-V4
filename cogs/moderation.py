from discord.ext import commands
from discord import Embed
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="clear")
    async def clear(self, ctx: SlashContext):
        await ctx.send("Clear!")


def setup(client):
    client.add_cog(Moderation(client))
