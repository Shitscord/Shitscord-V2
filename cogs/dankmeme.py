import discord, random
from discord.ext import commands
from cogs.cogfuncs import prawImage

class Dankmeme:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def dankmeme(self, ctx):
        await self.client.send_typing(ctx.message.channel)
        danksr=["dankmemes","okbuddyretard","dogelore","blessedimages","blursedimages","bonehurtingjuice","comedyheavan","cursedcomments","hmmtodayiwill","sbubby"]
        srfind=danksr[random.randint(0,len(danksr)-1)]
        embed = await prawImage.prawImgFind(subname=srfind)

        if not isinstance(embed, str):
            await self.client.send_message(ctx.message.channel, "test", embed=embed)


def setup(client):
    client.add_cog(Dankmeme(client))