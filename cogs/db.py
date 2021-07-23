from discord.ext import commands
from discord import Embed
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
import db


class DB(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
                        name="adduser",
                        description="Add a new user to the database",
                        guild_ids=[377169144648302597],
                        options=[
                            create_option(
                                name="new_user_id",
                                description="ID of the new user",
                                option_type=SlashCommandOptionType.INTEGER,
                                required=True),
                            create_option(
                                name="new_user_name",
                                description="Nickname of the new user",
                                option_type=SlashCommandOptionType.STRING,
                                required=True)
                        ])
    async def adduser(self, ctx: SlashContext, new_user_id: int, new_user_name: str):
        db.createuser(new_user_id, new_user_name)
        embed = Embed(title=f"User added", description=f"Added user '{new_user_name}' with ID {str(new_user_id)}'")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def removeuser(self, ctx, user_id: int):
        db.deleteuser(userid=user_id)
        await ctx.send(f"Deleted user {user_id}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def viewuser(self, ctx, user_nick: str):
        user = db.fetchuser(0, user_nick)
        if not user:  # If the returned value from fetchuser() is null, the user does not exist
            await ctx.send("Användaren finns ej")
        else:
            await ctx.send(f"ID: {user[0]}\nKB: {user[1]}\nNICK: {user[2]}")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def edituser(self, ctx, user_id: int, user_column: str, new_value: str):
        if user_column == "KB":
            db.edituser(user_id, user_column, int(new_value))
        else:
            db.edituser(user_id, user_column, new_value)

        await ctx.send(f"Ändrade {user_column} på {user_id} till {new_value}")


def setup(client):
    client.add_cog(DB(client))
