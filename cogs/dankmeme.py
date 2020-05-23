import discord, random
from discord.ext import commands
from cogs.cogfuncs import prawImage

class Dankmeme(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def dankmeme(self, ctx):
        async with ctx.message.channel.typing():
            danksr=["dankmemes","okbuddyretard","dogelore","blessedimages","blursedimages","bonehurtingjuice","comedyheavan","cursedcomments","hmmtodayiwill","sbubby"]
            srfind=danksr[random.randint(0,len(danksr)-1)]
            embed = await prawImage.prawImgFind(subname=srfind,sortby="default",srange="default",postType="default",)

        if not isinstance(embed, str):
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dankmeme(client))