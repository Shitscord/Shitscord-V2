import discord
from discord.ext import commands

class About:
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def about(self):
        await self.client.say("Shitscord v2, Developmental Version.\nCreated by TheWoneLolf. Use !help for commands.\nhttps://github.com/Shitscord/Shitscord-v2")
        
def setup(client):
    client.add_cog(About(client))