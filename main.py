from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
import db
import os

print("Loading...\n--------\n")

"""
SUB_COMMAND 1

SUB_COMMAND_GROUP 2

STRING 3

INTEGER 4

BOOLEAN 5

USER 6

CHANNEL 7

ROLE 8
"""

token = open("client_secret.txt", "r").read()

bot = commands.Bot(intents=Intents.all(), command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)
db.setup()


@bot.event
async def on_ready():
    print("Bot started")


# @client.command()
# async def load(_, extension):
#     client.load_extension(f'cogs.{extension}')
#
#
# @client.command()
# async def unload(_, extension):
#     client.unload_extension(f'cogs.{extension}')
#
#
# @client.command()
# async def reload(_, extension):
#     client.reload_extension(f'cogs.{extension}')


@slash.slash(name="ping", description="Fyfan vad coolt", guild_ids=[377169144648302597])
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency * 1000}ms)")


@slash.slash(name="test",
             guild_ids=[377169144648302597],
             description="This is just a test command, nothing more.",
             options=[
                 create_option(
                     name="optone",
                     description="This is the first option we have.",
                     option_type=SlashCommandOptionType.STRING,
                     required=False,
                     choices=[
                         create_choice(
                             name="ChoiceOne",
                             value="DOGE!"
                         ),
                         create_choice(
                             name="ChoiceTwo",
                             value="NO DOGE"
                         )
                     ]
                 )
             ])
async def test(ctx, optone: str):
    await ctx.send(content=f"Wow, you actually chose {optone}? :(")


if __name__ == "__main__":
    # for filename in os.listdir('./cogs'):
    #     if filename.endswith(".py"):
    #         bot.load_extension(f"cogs.{filename[:-3]}")
    #         print(f"Loaded {filename.strip('.py')}")
    bot.run(token)
