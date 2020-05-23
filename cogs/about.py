import discord, os
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def about(self, ctx):
        await ctx.send("Shitscord v2, Developmental Version.\nCreated by TheWoneLolf. Use !help for commands.\nhttps://github.com/Shitscord/Shitscord-v2", os.getenv("HEROKU_RELEASE_VERSION"))
        
def setup(client):
    client.add_cog(About(client))