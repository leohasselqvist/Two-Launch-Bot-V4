import discord
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
                                option_type=SlashCommandOptionType.STRING,
                                required=True),
                            create_option(
                                name="new_user_name",
                                description="Nickname of the new user",
                                option_type=SlashCommandOptionType.STRING,
                                required=True)
                        ])
    async def adduser(self, ctx: SlashContext, new_user_id: str, new_user_name: str):

        if new_user_id.isdigit():
            db.createuser(int(new_user_id), new_user_name)
            embed = Embed(title=f"User added", description=f"Added user '{new_user_name}' with ID {str(new_user_id)}")
        else:
            embed = Embed(title="Operation Failed", description="ID must only consist of numbers")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name="removeuser",
        description="Remove an existing user from the database",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="user_id",
                description="ID of the user",
                option_type=SlashCommandOptionType.STRING,
                required=True)
        ])
    async def removeuser(self, ctx: SlashContext, user_id: str):
        if user_id.isdigit():
            db.deleteuser(userid=int(user_id))
            embed = Embed(title=f"User removed", description=f"Removed user {user_id}")
        else:
            embed = Embed(title="Operation Failed", description="ID must only consist of numbers")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name="viewuser",
        description="View an existing user in the database",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="user",
                description="User to view",
                option_type=SlashCommandOptionType.USER,
                required=True)
        ])
    async def viewuser(self, ctx, user: discord.User):
        db_user = db.fetchuser(0, user.display_name)
        if not db_user:  # If the returned value from fetchuser() is null, the user does not exist
            embed = Embed(title="Could not find user", description=f"The user '{user.display_name}' could not be found.")
        else:
            embed = Embed(title=db_user[2], description=f"**ID:** {db_user[0]}\n**KB:** {db_user[1]}\n")
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name="edituser",
        description="Add a new user to the database",
        guild_ids=[377169144648302597],
        options=[
            create_option(
                name="user_id",
                description="ID of the user",
                option_type=SlashCommandOptionType.STRING,
                required=True),
            create_option(
                name="user_column",
                description="Which attribute to edit",
                option_type=SlashCommandOptionType.STRING,
                required=True,
                choices=["ID", "KB", "NICK"]),
            create_option(
                name="new_value",
                description="What the new value should be",
                option_type=SlashCommandOptionType.STRING,
                required=True)
        ])
    async def edituser(self, ctx, user_id: str, user_column: str, new_value: str):
        if user_id.isdigit():
            user_id = int(user_id)
        else:
            await ctx.send(
                embed=Embed(title="Operation Failed", description="ID must only consist of numbers")
            )
            return

        if user_column == "KB":
            db.edituser(user_id, user_column, int(new_value))
        else:
            db.edituser(user_id, user_column, new_value)

        embed = Embed(title=f"Edited user", description=f"Changed '{user_column}' on ID {str(user_id)} to {new_value}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(DB(client))
