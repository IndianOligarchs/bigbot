import discord
from discord.ext import commands

class MyHelpCommand(commands.HelpCommand):
        # This function triggers when somone type `<prefix>help`
    async def send_bot_help(self, mapping):
            ctx = self.context
            embed = discord.Embed(color=discord.Color.blurple())
            embed.add_field(name='To get more info on the modules:', value=f'Send ``{self.clean_prefix}help [Module Name]`` for more info on each module, please remember to capitalize the first letter of the module.')
            embed.set_author(name='BigBot Help')
            ctx.bot.cogs
            for cog in ctx.bot.cogs:
                    if cog == 'Jishaku':
                            h = 'f'
                    else:
                            embed.add_field(name=cog, value=ctx.bot.cogs[cog].description, inline=False)
            await ctx.send(embed=embed)
    
    # This function triggers when someone type `<prefix>help <cog>`
    async def send_cog_help(self, cog):
            ctx = self.context
            if cog == 'jishaku':
                    return
            else:
                    embed = discord.Embed(color=discord.Color.blurple())
                    embed.set_author(name=f'{cog.qualified_name} Help')
                    embed.add_field(name='Key:', value='```<> = optional argument\n[] = required argument\nDo not type [] or <> during a command.```')
 
                    for thing in cog.get_commands():
                            embed.add_field(name=thing.qualified_name, value=f'Description: {thing.help}\nUsage: {self.clean_prefix}{thing.qualified_name} {thing.signature}', inline=False)
                    await ctx.send(embed=embed)
            # Do what you want to do here
    
    async def send_command_help(self, command):
            ctx = self.context
            embed = discord.Embed(color=discord.Color.blue())
            embed.set_author(name=f'{command.qualified_name} Help')
            embed.add_field(name=f'Usage: {self.clean_prefix}{command.qualified_name} {command.signature}', value=f'Description: {command.help}', inline=False)

            embed.add_field(name='Key:', value='```<> = optional argument\n[] = required argument\nDo not type [] or <> during a command.```')
            await ctx.send(embed=embed)

    async def send_group_help(self, group):
            ctx = self.context
            embed = discord.Embed(color=discord.Color.dark_purple())
            embed.set_author(name=f'{group.qualified_name} Help')
            for thing in group.commands:
                embed.add_field(name=thing.qualified_name, value=f'Description: {thing.help}\nUsage: {self.clean_prefix}{thing.qualified_name} {thing.signature}', inline=False)
            await ctx.send(embed=embed)
            
                
class Help(commands.Cog):
    """Shows this command, allows for in-depth explanations."""
    def __init__(self, bot):
        self.bot = bot
        
        # Storing main help command in a variable
        self.bot._original_help_command = bot.help_command
        
        # Assiginig new help command to bot help command
        bot.help_command = MyHelpCommand()
        
        # Setting this cog as help command cog
        bot.help_command.cog = self
        
        # Event triggers when this cog unloads
    def cog_unload(self):
                
        # Setting help command to the previous help command so if this cog unloads the help command restores to previous
        self.bot.help_command = self.bot._original_help_command

def setup(bot):
        bot.add_cog(Help(bot))


