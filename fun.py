import discord
from discord.ext import commands, tasks
import json
import aiohttp
import random
import asyncpraw






class Fun(commands.Cog):
    """Commands in the "fun" section are entertainment, with commands such as meme, randomfact, and mcskin. **Provides Updates Weekly**."""

    def __init__(self, bot):
        self.bot = bot
        self.memes = []
        self.refresh.start()
        self.dankmemes = []

    @commands.command()
    async def mcskin(self, ctx, username):
        """Gives the mcskin of a username."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{username}') as r:
                res = await r.json()
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.set_author(name=f"{username}'s Skin")
                embed.set_image(url=f"https://crafatar.com/renders/body/{res['id']}")
                await ctx.send(embed=embed)


    @commands.command(aliases=['uselessfact'])
    async def randomfact(self, ctx):
        """Sends a random/useless fact"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://uselessfacts.jsph.pl/random.json?language=en') as r:
                res = await r.json()
                await ctx.send(res['text'])
    

    @tasks.loop(seconds=420)
    async def refresh(self):
        subreddit = await self.bot.reddit.subreddit("memes")
        redposts = []
        posts = subreddit.hot(limit=60)
        async for post in posts:
            redposts.append(post)
        self.memes = redposts
        subredditdank = await self.bot.reddit.subreddit("dankmemes")
        dankposts = []
        dposts = subredditdank.hot(limit=60)
        async for dpost in dposts:
            dankposts.append(dpost)
        self.dankmemes = dankposts              
            
    @commands.command()
    async def meme(self, ctx):
        """Gets a random meme from reddit and posts it."""
        redpost = random.choice(self.memes)
        self.memes.remove(redpost)
        if redpost.is_self is True:
            redpost = random.choice(self.memes)
        title = redpost.title
        link = redpost.url
        img_url = redpost.url
        embed = discord.Embed(title=title, url=link)
        embed.set_image(url=img_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction('\U0001f44d')
        await message.add_reaction('\U0001f44e')


    @commands.command()
    async def dankmeme(self, ctx):
        """Gets a random *dank* meme from reddit and posts it."""
        redpost = random.choice(self.dankmemes)
        self.dankmemes.remove(redpost)
        title = redpost.title
        link = redpost.url
        img_url = redpost.url
        embed = discord.Embed(title=title, url=link)
        embed.set_image(url=img_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction('\U0001f44d')
        await message.add_reaction('\U0001f44e')

def setup(bot):
    bot.add_cog(Fun(bot))
