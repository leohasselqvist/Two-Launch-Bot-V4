from discord.ext import commands
import db


class DB(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role(616590353709006859)
    @commands.command()
    async def adduser(self, ctx, new_user_id: int, new_user_name: str):
        db.createuser(new_user_id, new_user_name)
        await ctx.send("Skapade en ny användare, " + new_user_name)

    @commands.has_role(616590353709006859)
    @commands.command()
    async def removeuser(self, ctx, user_id: int):
        db.deleteuser(userid=user_id)
        await ctx.send(f"Deleted user {user_id}")

    @commands.has_role(616590353709006859)
    @commands.command()
    async def viewuser(self, ctx, user_nick: str):
        user = db.fetchuser(0, user_nick)
        if not user:  # If the returned value from fetchuser() is null, the user does not exist
            await ctx.send("Användaren finns ej")
        else:
            await ctx.send(f"ID: {user[0]}\nKB: {user[1]}\nNICK: {user[2]}")

    @commands.has_role(616590353709006859)
    @commands.command()
    async def edituser(self, ctx, user_id: int, user_column: str, new_value: str):
        if user_column == "KB":
            db.edituser(user_id, user_column, int(new_value))
        else:
            db.edituser(user_id, user_column, new_value)

        await ctx.send(f"Ändrade {user_column} på {user_id} till {new_value}")


def setup(client):
    client.add_cog(DB(client))
