from discord.ext import commands
from discord import Embed
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle


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
        await ctx.send(f"Are you sure you want to clear {amount} messages?", components=[
            create_actionrow(
                create_button(
                    style=ButtonStyle.red,
                    label="Cancel"
                ),
                create_button(
                    style=ButtonStyle.blue,
                    label="Confirm"
                ),
            )
        ])


def setup(client):
    client.add_cog(Moderation(client))
