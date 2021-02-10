import discord
from discord.ext import commands
import datetime
from datetime import date
import regex as re
import os
import json

class Info(commands.Cog):
    """These commands are meant for learning more about the bot."""
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(color=discord.Color.gold(), title='Bigbot Support Server', description='[Click Here](https://discord.gg/da3jdR5)')
        await ctx.send(embed=embed)



    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(), title='Bigbot Info')
        embed.add_field(name='Owner:', value='nope#8182')
        embed.add_field(name='Support Server:', value='[Click Here](https://discord.gg/da3jdR5)')
        embed.add_field(name='Stats', value=f'Users: {len([*self.bot.get_all_members()])}\nServers:{len(self.bot.guilds)}')
        embed.add_field(name='Support Us', value='[Here](https://top.gg/bot/719727622782845031), [Here](https://discordbotlist.com/bots/bigbot), and [Here](https://discord.bots.gg/bots/719727622782845031)')
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """This command shows how long the bot has been running."""
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"I have been online for: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.")


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong:{int(self.bot.latency * 1000)}ms is my ping.')

    


    @commands.command()
    async def servers(self, ctx):
        """This command will give you information on the amount of servers this bot is in. The owner of this bot may see each server however for privacy reasons you may not."""
        if ctx.author.id == 713979128969429012:
            await ctx.send(f':white_check_mark: {ctx.author.mention}, please check terminal or your direct messages.')
            for guild in self.bot.guilds:
                await ctx.author.send(guild.name)
                print(guild.name)
        else:
            await ctx.send(f':x: {ctx.author.mention}, for privacy reasons only the bot owner may see a list of servers, for a total count of servers, the number is {len(self.bot.guilds)}')


def setup(bot):
    bot.add_cog(Info(bot))
        
