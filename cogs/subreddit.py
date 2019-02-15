import discord, random
from discord.ext import commands
from cogs.cogfuncs import prawImage

class Subreddit:
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    async def subreddit(self, ctx):
        await self.client.send_typing(ctx.message.channel)
        commandList=str(ctx.message.content).split()

        optDict={}

        if len(commandList) >= 2:
            optDict["subname"]=commandList[1]
        
        #Get parameter: Sort by
        if "-s" in commandList: 
            if commandList.index("-s")+1<len(commandList):
                tempParam = commandList[commandList.index("-s")+1]
            else:
                tempParam = None
            optDict["sortby"] = tempParam

        #Get parameter: Random range
        if "-r" in commandList: 
            if commandList.index("-r")+1<len(commandList):
                tempParam = commandList[commandList.index("-r")+1]
            else:
                tempParam = None
            optDict["srange"]

        print(optDict)
        embed = await prawImage.prawImgFind(**optDict)
        await self.client.send_message(ctx.message.channel, embed=embed)


def setup(client):
    client.add_cog(Subreddit(client))