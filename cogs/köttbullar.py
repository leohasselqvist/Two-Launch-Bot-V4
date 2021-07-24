from discord.ext import commands
import discord
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

    @commands.command(aliases=["mata", "feed"])
    async def kbsend(self, ctx, *args):
        sender = ctx.message.author
        amount = int(args[0])
        try:
            receiver = self.discord_id_check(args[1])
        except IndexError:
            receiver = None
        reason = ""
        for word in args[2:len(args)]:
            reason += word + " "

        if sender != receiver:
            try:
                db.KB.send(sender.id, receiver.id, amount, reason)
                await ctx.send(f"Skickade {amount} köttbullar till {receiver.display_name}")
            except AttributeError:
                db.KB.send(sender.id, db.fetchuser(0, nick=receiver)[0], amount, reason)
                await ctx.send(f"Skickade {amount} köttbullar till {receiver}")
            except IndexError:
                await ctx.send("Du får steka mer köttbullar, du har för få för det där.")
        else:
            await ctx.send("Du kan inte skicka köttbullar till dig själv")

    @commands.command()
    async def kb(self, ctx, *args):
        try:
            other = self.discord_id_check(args[0])
        except IndexError:
            other = None

        if other:
            try:
                await ctx.send(f"{other.display_name} har {str(db.fetchuser(other.id)[1])} köttbullar i pannan")
            except AttributeError:
                await ctx.send(f"{other} har {str(db.fetchuser(0, nick=other)[1])} köttbullar i pannan")
        else:
            await ctx.send(f"Du har {str(db.fetchuser(ctx.message.author.id)[1])} köttbullar i pannan")

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
