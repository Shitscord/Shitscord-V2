import discord, os
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def about(self, ctx):
        await ctx.send("Build Name: "+ str(os.getenv("HEROKU_APP_NAME")) + ". Build Version: " + str(os.getenv("HEROKU_RELEASE_VERSION")) + ".\nShitscord Rewrite. Created by TheWoneLolf.\n Use !help for commands.\nhttps://github.com/Shitscord/Shitscord-v2" )
        
def setup(client):
    client.add_cog(About(client))