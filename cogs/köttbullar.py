from discord.ext import commands
import discord
from discord import Embed
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from sqlite3 import IntegrityError
import db

db.setup()


class Kottbullar(commands.Cog):
    def __init__(self, client):
        self.client = client

    def discord_id_check(self, other):
        if other.startswith("<@"):
            other = ''.join(filter(str.isdigit, other))  # Jobbig rad, filtrerar bort alla ickenummer i args[0]
            for server in self.client.guilds:  # Fanns säker ett bättre sätt att få användaren men jag orkar fan ej
                for user in server.members:
                    if str(user.id) == other:
                        other = user
        return other

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.client.guilds:
            for user in server.members:
                try:
                    db.createuser(user.id, user.display_name)
                    db.edituser(user.id, "NICK", user.display_name)
                except IntegrityError:
                    pass

    @cog_ext.cog_slash(
        name="kbsend",
        description="Send someone your KB",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="amount",
                description="Amount of Kb to be sent",
                option_type=SlashCommandOptionType.INTEGER,
                required=True),
            create_option(
                name="receiver",
                description="User to send KB to",
                option_type=SlashCommandOptionType.USER,
                required=True),
            create_option(
                name="reason",
                description="(Optional) Reason for payment",
                option_type=SlashCommandOptionType.STRING,
                required=False)
        ])
    async def kbsend(self, ctx, amount: int, receiver: discord.User, reason="No reason"):
        sender = ctx.author
        #amount = int(args[0])
        #try:
        #    receiver = self.discord_id_check(args[1])
        #except IndexError:
        #    receiver = None
        #reason = ""
        #for word in args[2:len(args)]:
        #    reason += word + " "

        if sender != receiver:
            try:
                db.KB.send(sender.id, receiver.id, amount, reason)
                embed = Embed(title="KB Sent!",
                              description=f"Sent {amount} KB to {receiver.display_name} for '{reason}'",
                              color=0x00ff00
                              )
            except IndexError:
                embed = Embed(title="Send KB Error",
                              description="You don't have enough KB",
                              color=0xff0000,
                              hidden=True)
        else:
            embed = Embed(title="Send KB Error",
                          description="You can't send KB to yourself, silly goose.",
                          color=0xff0000,
                          hidden=True)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="kb",
        description="Check your own or someone else's köttbullar",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="user",
                description="(Optional) Other user to view",
                option_type=SlashCommandOptionType.USER,
                required=False)
        ])
    async def kb(self, ctx, user=None):
        if user is None:  # If there was no user specified
            user = ctx.author  # The user to check will be the author of the message
        embed = Embed(
            title="Bank of KB",
            description=f"{user.display_name} har {str(db.fetchuser(user.id)[1])} köttbullar i pannan"
            # Line above grabs the user's table from the db, then grabs column 1, the one that stores KB.
        )
        await ctx.send(embed=embed)

    @kb.error
    async def kb_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Du måste tagga personen")
        else:
            await ctx.send(f"Okänt fel för ``;kb``: ``{error}``")
            raise error

    @kbsend.error
    async def kbsend_error(self, ctx, error):
        print(error)
        if isinstance(error, IndexError):
            await ctx.send("Du saknar credits")
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Kommandot är felskriven, skriv så här:\n``;kbsend [mängd] [användare] [skäl]``")
        else:
            await ctx.send(f"Okänt fel för ``kbsend``: ``{error}``")
            raise error

    @cog_ext.cog_slash(
        name="kbhistory",
        description="Check your KB transfer history",
        guild_ids=[377169144648302597]
    )
    async def kbhistory(self, ctx):
        user = ctx.author  # The user to check will be the author of the message
        embed = Embed(
            title="Bank of KB",
            description=f"{db.fetchhistory(user.id)}"
            # Line above grabs the user's table from the db, then grabs column 1, the one that stores KB.
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(616590353709006859)
    async def kbmasstransfer(self, ctx, amount: int):
        db.KB.transferall(amount)
        await ctx.send(f"La till {amount} KB till alla")

    @commands.command()
    @commands.has_role(616590353709006859)
    async def kbmassremove(self, ctx, amount: int):
        db.KB.removeall(amount)
        await ctx.send(f"Tog bort {amount} KB från alla")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if before.nick != after.nick:
                db.edituser(after.id, "NICK", after.nick)
        except AttributeError:
            pass


def setup(client):
    client.add_cog(Kottbullar(client))
