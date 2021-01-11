import discord
import asyncio
from discord.ext import commands
from datetime import date
from datetime import timedelta
import json
import random
import typing
import datetime
from datetime import date
import asyncpg
import string

class Moderation(commands.Cog):
    """Commands for all your moderation needs. **Provides Updates Weekly**."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: typing.Optional[discord.Member], *, reason = None):
        """Warns a user and adds a warn to their record accessible by using the search [member] command."""
        if reason == None:
            reason = "No Reason Provided, Moderator, please use the reason [case id] [reason] command to provide a reason."
        else:
            reason = reason
        def get_random_string(length):
            # Random string with the combination of lower and upper case
            letters = string.ascii_letters
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str
            
        connection = await self.bot.pg_con.acquire()
        async with connection.transaction():
            sql = ("INSERT INTO warns(user_id, warn_reason, guild_id, case_id, case_date, warner_id) VALUES ($1,$2,$3,$4,$5,$6)")
            await connection.execute(sql, member.id, reason, ctx.guild.id, get_random_string(5), datetime.datetime.utcnow(), ctx.author.id)
        await self.bot.pg_con.release(connection)

        await ctx.send(f"Warned {member.mention} for {reason}.")
        await member.send(f"You were warned in {ctx.guild.name} for {reason}.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def reason(self, ctx, caseid, *, reason):
        """Updates the reason for the provided caseid"""
        conn = await self.bot.pg_con.acquire()
        async with conn.transaction():
            await conn.execute('UPDATE warns SET warn_reason = $1 WHERE case_id = $2', reason, caseid)
        await self.bot.pg_con.release(conn)
        await ctx.send(f'Updated the reason of case {caseid} to ``{reason}``.')
    
    @commands.command()
    async def search(self, ctx, member: typing.Optional[discord.Member]):
        """Shows a user's moderation record."""
        if member == None:
            member = ctx.author
        else: 
            member = member
        async with self.bot.pg_con.acquire() as con:
            casenum = await con.fetch('SELECT case_id FROM warns where user_id = $1 and guild_id = $2', member.id, ctx.guild.id)
        embed = discord.Embed(colour = discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'Warn history for {member.mention}:')
        embed.set_thumbnail(url=member.avatar_url)
        async with self.bot.pg_con.acquire() as con:
            for case in casenum:
                date = await con.fetch('SELECT case_date FROM warns where user_id = $1 and guild_id = $2 and case_id = $3', member.id, ctx.guild.id, case[0])
                result = await con.fetch('SELECT warn_reason FROM warns where user_id = $1 and guild_id = $2 and case_id = $3 and case_date = $4', member.id, ctx.guild.id, case[0], date[0][0])
                warner = await con.fetch('SELECT warner_id FROM warns where user_id = $1 and guild_id = $2 and case_id = $3 and case_date = $4 and warn_reason = $5', member.id, ctx.guild.id, case[0], date[0][0], result[0][0])
                warner = await self.bot.fetch_user(warner[0][0])
                embed.add_field(name='Warn', value=f'**Reason:** {result[0][0]}\n **Case ID:** {case[0]}\n **Date:** {date[0][0]}\n **Warner:** {warner.mention}', inline = False)
        await ctx.send(embed=embed)
        


            
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx, case_id):
        """Removes a warn from a user."""
        connection = await self.bot.pg_con.acquire()
        async with connection.transaction():
            await self.bot.pg_con.execute('DELETE FROM warns where case_id = $1 and guild_id = $2', case_id, ctx.guild.id,)
        await self.bot.pg_con.release(connection)
        await ctx.send(f'Removed the warn from the user.')
    

    #brokenish
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: typing.Optional[discord.Member], mute_time : typing.Optional[str]):
        """Mutes the user for the specified amount of time, defaults to infinity if no time is provided. Makes them not able to talk in any channels. Requires kick_members."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role is None:
            role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(send_messages=False))
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False)
        if mute_time is None:
            await member.add_roles(role)
            await ctx.send(f'**Muted {member.mention}.**')
            return
        else:
            typetime = mute_time[-1]
            mute_time = int(mute_time[:-1])
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not member and not mute_time and not typetime:
                await ctx.send("Who do you want me to mute?")
                return
            if typetime == "h" or typetime == "hours":
                mute_time1 = mute_time * 3600
                typetime = "hours"
            elif typetime == "m" or typetime == "minutes":
                mute_time1 = mute_time * 60
                typetime = "minutes"
            elif typetime == "w" or typetime == "weeks":
                mute_time1 = mute_time * 604800
                typetime = "weeks"
            elif typetime == "s" or typetime == "seconds":
                typetime = "seconds"
                mute_time1 = mute_time * 1
            await member.add_roles(role)
            await ctx.send(f'**Muted {member.mention} for {mute_time} {typetime}.**')
            await asyncio.sleep(mute_time1)
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f'**Unmuted {member.mention}.**')  
            else:
                return



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: typing.Optional[discord.Member]):
        """Unmutes the user. Makes them able to talk in channels again. Requires kick_members."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role not in member.roles:
            await ctx.send("**User is not muted.**")
        else:
            await member.remove_roles(role)
            await ctx.send(f'**Unmuted {member.mention}.**')


    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: typing.Optional[discord.Member], *, reason = None):
        """Kicks the user. Removes them from the guild/server. Requires kick_members."""
        guild = ctx.guild
        if member.top_role > guild.me.top_role:
            await ctx.send("I'm sorry, I don't have permission to kick this user.")
            return
        else:  
            if reason == None:
                await member.send("**You have been kicked from " + ctx.guild.name + ".**")
                await ctx.send("Kicked " + member.mention + ".")
            else:
                await member.send("**You have been kicked from " + ctx.guild.name + " for " + reason + ".**")
                await ctx.send("Kicked " + member.mention + " for " + reason + ".")
            await ctx.guild.kick(member, reason=reason)
   

    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: typing.Optional[discord.Member], *, reason = None):
        """Bans the user. Removes them from the guild/server and makes them unable to join. Requires ban_members."""
        guild = ctx.guild
        if member.top_role > guild.me.top_role:
            await ctx.send("I'm sorry, I don't have permission to ban this user.")
            return
        else:  
            if reason == None:
                await member.send("**You have been banned from " + ctx.guild.name + ".**")
                await ctx.send("Banned " + member.mention + ".")
            else:
                await member.send("**You have been banned from " + ctx.guild.name + " for " + reason + ".**")
                await ctx.send("Banned " + member.mention + " for " + reason + ".")
            await ctx.guild.ban(member, reason=reason)


    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid: typing.Optional[discord.User], *, reason = None):
        """Unbans the user. Allows them to join the guild/server again. Requires ban_members."""
        if reason == None:
            await ctx.send("Unbanned " + userid.mention + ".")
        else:
            await ctx.send("Unbanned " + userid.mention + " for "  + reason + ".")
        await ctx.guild.unban(userid)



    #brokenish
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, lockedchannel: typing.Optional[discord.TextChannel], *, reason=None):
        """Locks the channel. Requires a user to have administrator to talk in the channel. Requires administrator."""
        guild = ctx.guild
        if lockedchannel == None:
            channel = ctx.channel
        else:
            channel = lockedchannel
        await channel.set_permissions(guild.default_role, send_messages=False)
        if reason == None:
            await ctx.send(f'Locked {channel.mention}.')
        else:
            await ctx.send(f'Locked {channel.mention} for {reason}.')


    #brokenish
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, lockedchannel: typing.Optional[discord.TextChannel], *, reason=None):
        """Unlocks the channel. Removes the requirement of administrator to talk in the channel."""
        guild = ctx.guild
        if lockedchannel == None:
            channel = ctx.channel
        else:
            channel = lockedchannel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
  
        }  


    
    @commands.command(name='purge')
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=0):
        """Deletes the specified amount of messages in the channel. Requires administrator permissions."""
        amount = int(amount)
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


 


def setup(bot):
    bot.add_cog(Moderation(bot))
