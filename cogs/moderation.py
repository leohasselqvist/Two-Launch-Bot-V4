from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
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
        delete_message = await ctx.send(f"Are you sure you want to clear {amount} messages?", components=[confirmation_actionrow])
        button_ctx: ComponentContext = await wait_for_component(self.bot, components=confirmation_actionrow)
        if button_ctx.custom_id == "buttonConfirm":
            await delete_message.edit(content=f"Cleared {amount} messages!", components=[])
        else:
            await delete_message.edit(content="Cancelling clear command...", components=[])
        await delete_message.delete(delay=10)


def setup(client):
    client.add_cog(Moderation(client))
