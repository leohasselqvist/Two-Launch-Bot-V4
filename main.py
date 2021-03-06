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
        await ctx.send(f"{extension.capitalize()} cog loaded!")
    except commands.errors.ExtensionAlreadyLoaded:
        await ctx.send(f"{extension.capitalize()} cog is already loaded")


@slash.slash(name="unload",
             description="Unload a previously loaded extension to the bot",
             guild_ids=[377169144648302597],
             options=[
                 create_option(
                     name="extension",
                     description="Name of the extension to unload",
                     option_type=SlashCommandOptionType.STRING,
                     required=True,
                     choices=cogs_list
                 )
             ])
@commands.is_owner()
async def unload(ctx, extension: str):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension.capitalize()} cog unloaded!")
    except commands.errors.ExtensionNotLoaded:
        await ctx.send(f"{extension.capitalize()} cog is already unloaded.")


@slash.slash(name="reload",
             description="Reload an already loaded extension to the bot",
             guild_ids=[377169144648302597],
             options=[
                 create_option(
                     name="extension",
                     description="Name of the extension to reload",
                     option_type=SlashCommandOptionType.STRING,
                     required=True,
                     choices=cogs_list
                 )
             ])
@commands.is_owner()
async def reload(ctx, extension: str):
    try:
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension.capitalize()} cog reloaded!")
    except commands.errors.ExtensionNotLoaded:
        await ctx.send(f"You can not reload an unloaded cog.")


@slash.slash(name="ping", description="Fyfan vad coolt", guild_ids=[377169144648302597])
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency * 1000}ms)")


@bot.event
async def on_ready():
    print("Bot started")

bot.run(token)
