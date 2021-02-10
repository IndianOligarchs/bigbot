import discord
from discord.ext import commands
import datetime
from datetime import date
import regex as re
import os
import json

class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    """These commands are meant for the owner only.."""
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.group()
    @commands.is_owner()
    async def dev(self, ctx):
        return



    @dev.command()
    @commands.is_owner()
    async def reboot(self, ctx):
        await ctx.send(':gear: Rebooting now. :gear:')
        await self.bot.close()

    @dev.command()
    @commands.is_owner()
    async def presence(self, ctx, *, presence):
        await self.bot.change_presence(activity=discord.Game(name=presence))
        await ctx.send(':white_check_mark: Changed the presence!')


    @dev.command()
    @commands.is_owner() 
    async def reload(self, ctx, extension):
        """This is a bot owner only command."""
        self.bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}.')
    
    @reload.error
    async def reload_error(self, ctx, error):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=str(error))
        await ctx.send(embed=embed)




    @dev.command() 
    @commands.is_owner()
    async def reloadall(self, ctx):
        """This is a bot owner only command."""
        for file in os.curdir: 
            if file.endswith(".py"):
                name = file[:-3]
                self.bot.reload_extension(f'cogs.{name}')
                await ctx.send(f'Reloaded {name}.')


    @reloadall.error
    async def reloadall_error(self, ctx, error):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=str(error))
        await ctx.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def addall(self, ctx):
        for guild in self.bot.guilds:
            connection = await self.bot.pg_con.acquire()
            async with connection.transaction():
                await connection.execute('INSERT INTO config (guild_id, automod, logging) VALUES($1, $2, $3)', guild.id, False, False)
            await self.bot.pg_con.release(connection) 




    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        connection = await self.bot.pg_con.acquire()
        async with connection.transaction():
            await connection.execute('INSERT INTO prefixes (guild_id, prefix) VALUES($1, $2)', guild.id, '-')
            await connection.execute('INSERT INTO config (guild_id, automod, logging) VALUES($1, $2, $3)', guild.id, False, False)
        await self.bot.pg_con.release(connection)
        user = self.bot.get_user(713979128969429012)
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow(), title=':tada: NEW GUILD! :tada:', description=f'We now have {len(self.bot.guilds)} guilds!!')
        await user.send(embed=embed)

    

    @commands.Cog.listener()
    async def on_message(self, message):
        if re.search(rf'^<@!?719727622782845031>$', message.content):       
            connection = await self.bot.pg_con.acquire()
            async with connection.transaction():
                prefix = await connection.fetch('SELECT prefix FROM prefixes WHERE guild_id = $1', message.guild.id)
            await self.bot.pg_con.release(connection)

            await message.channel.send(f"{message.author.mention} my prefix in this server is: {prefix[0][0]}.")

    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        connection = await selfbot.pg_con.acquire()
        async with connection.transaction():
            await connection.execute('DELETE FROM prefixes WHERE guild_id = $1', guild_id)
        await self.bot.pg_con.release(connection)



def setup(bot):
    bot.add_cog(Owner(bot))
