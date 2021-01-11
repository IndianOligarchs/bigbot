import discord
from discord.ext import commands
import datetime
from datetime import date
import regex as re
import os
import json


class Config(commands.Cog):
    """These commands are meant for administative duties and customizing the bot."""
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx):
        connection = await self.bot.pg_con.acquire()
        async with connection.transaction():
            prefixn = await connection.fetch('SELECT prefix FROM prefixes WHERE guild_id = $1', ctx.guild.id)
        await self.bot.pg_con.release(connection)
        await ctx.send(f"{ctx.guild.name}'s prefix is: {prefixn[0][0]}.")

    
    @prefix.command()
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def set(self, ctx, prefix = None):
        """This command sets the bot's prefix for the server only. Requires administrator."""
        connection = await self.bot.pg_con.acquire()
        async with connection.transaction():
            await connection.execute('UPDATE prefixes SET prefix = $1 WHERE guild_id = $2', prefix, ctx.guild.id)
        await self.bot.pg_con.release(connection)
        await ctx.send(f'Updated the prefix to {prefix}.')



    


    

   

def setup(bot):
    bot.add_cog(Config(bot))
        






