from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
import db
import os

print("Loading...\n--------\n")

token = open("client_secret.txt", "r").read()
bot = commands.Bot(intents=Intents.all(), command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)
cogs_list = []
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        cogs_list.append(create_choice(name=filename[:-3].capitalize(), value=filename[:-3]))
        print(f"Loaded {filename.strip('.py')}")

db.setup()


@bot.event
async def on_ready():
    print("Bot started")


@slash.slash(name="load",
             description="Load a previously unloaded extension to the bot",
             guild_ids=[377169144648302597],
             options=[
                 create_option(
                     name="extension",
                     description="Name of the extension to load",
                     option_type=SlashCommandOptionType.STRING,
                     required=True,
                     choices=cogs_list
                 )
             ])
@commands.is_owner()
async def load(ctx, extension: str):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} cog loaded!")
    except commands.errors.ExtensionAlreadyLoaded:
        await ctx.send(f"{extension} cog is already loaded", hidden=True)


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

bot.run(token)
