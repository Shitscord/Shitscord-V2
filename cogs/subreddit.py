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

        prawReady = True
        optDict={}

        if len(commandList) <2:
            textReturn = "Please enter a subreddit."
            prawReady = False
        else:
            optDict["subreddit"]=commandList[1]
        
        #Get parameter: Sort by
        if "-s" in commandList: 
            if commandList.index("-s")+1<len(commandList):
                optDict["sortby"] = commandList[commandList.index("-s")+1]
            else:
                textReturn = "Enter a sorting method after '-s'. Default: Hot"
                prawReady = False

        #Get parameter: Random range
        if "-r" in commandList: 
            if commandList.index("-r")+1<len(commandList):
                optDict["srange"] = commandList[commandList.index("-r")+1]
            else:
                textReturn = "Enter a range after '-s'. Default: 100"
                prawReady = False

        if prawReady:
            textReturn = await prawImage.prawImgFind(**optDict)
            if textReturn == "no_sub":
                textReturn = "Invalid subreddit."
            elif textReturn == "no_image":
                textReturn = "No images could be found."
            elif textReturn == "no_sort":
                textReturn = "Specify an appropriate value for -s"
            elif textReturn == "retries_not_int":
                textReturn = "Specify a number for -c"

        await self.client.say(textReturn)


def setup(client):
    client.add_cog(Subreddit(client))