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
db.setup()


@slash.slash(name="ping", description="Fyfan vad coolt", guild_ids=[377169144648302597])
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency * 1000}ms)")


@bot.event
async def on_ready():
    print("Bot started")

bot.run(token)
