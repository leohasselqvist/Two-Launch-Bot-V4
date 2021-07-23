from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import db
import os

print("Loading...\n--------\n")

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


@slash.slash(name="ping")
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")


if __name__ == "__main__":
    # for filename in os.listdir('./cogs'):
    #     if filename.endswith(".py"):
    #         bot.load_extension(f"cogs.{filename[:-3]}")
    #         print(f"Loaded {filename.strip('.py')}")
    bot.run(token)
