import asyncio

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
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
        confirmation_actionrow = create_actionrow(
            create_button(
                style=ButtonStyle.blue,
                label="Confirm",
                custom_id="buttonConfirm"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Cancel",
                custom_id="buttonCancel"
            ),
        )

        def is_not_bot(m):
            return m.author != self.bot.user

        delete_message = await ctx.send(f"Are you sure you want to clear {amount} messages?", components=[confirmation_actionrow])
        try:
            button_ctx: ComponentContext = await wait_for_component(self.bot, components=confirmation_actionrow, timeout=10)
            if button_ctx.custom_id == "buttonConfirm":
                await delete_message.edit(content=f"Cleared {amount} messages!", components=[])
                await ctx.channel.purge(limit=amount + 1, check=is_not_bot)
            else:
                await delete_message.edit(content="Cancelled clear command.", components=[])
            await delete_message.delete(delay=2)
        except asyncio.TimeoutError:
            await delete_message.delete()


def setup(client):
    client.add_cog(Moderation(client))
