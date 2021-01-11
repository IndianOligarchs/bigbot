import discord
import traceback
from discord.ext import commands
from discord import Intents
import asyncpg
import regex
import logging
import typing
import random
import datetime 
from datetime import date
import json
import asyncpraw
intents = Intents.all()
token = 'NzE5NzI3NjIyNzgyODQ1MDMx.Xt7olQ.GDkXga6bXn9yrypKBgoWzYQsuQk'
async def get_prefix(bot, message):

    connection = await bot.pg_con.acquire()
    async with connection.transaction():
        prefix = await connection.fetch('SELECT prefix FROM prefixes WHERE guild_id = $1', message.guild.id)
    await bot.pg_con.release(connection)
    return prefix[0][0]


#te
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, activity=discord.Game(name='Bigbot'))
bot.launch_time = datetime.datetime.utcnow()

bot.reddit = asyncpraw.Reddit(client_id='w0Dhd8yns9ck3g',
                    client_secret ='JSlJMG8Adi_co3UslcTuHNYrka0',
                    username='Comfortable-Award650',
                    password='kris1213',
                    user_agent='prawtutv1')


initial_extensions = ['cogs.moderation',
                     'cogs.help',
                     'cogs.config',
                     'cogs.fun',
                     'cogs.owner',
                     'cogs.info'
                     ]

if __name__ == '__main__':
    bot.load_extension('jishaku')
    for extension in initial_extensions:
        bot.load_extension(extension)
    print('All cogs have been loaded!')



@bot.event
async def on_ready():
    print('Running')




async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database='warns', user='admin', password='kris1213K')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'You are missing the correct permissions to run this command. You need {error.missing_perms[0]}.')
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'You are missing the correct permissions to run this command. You need to own this bot.')
        await ctx.send(embed=embed)
    else:
        etype = type(error)
        trace = error.__traceback__
        lines = traceback.format_exception(etype, error, trace)
        traceback_text = ''.join(lines)
        channel = bot.get_channel(796239640961089566)
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow(), title='ERROR', description=f'An error has occured: ```{traceback_text}```')
        await channel.send(embed=embed)



bot.loop.run_until_complete(create_db_pool())    
bot.run(token)




