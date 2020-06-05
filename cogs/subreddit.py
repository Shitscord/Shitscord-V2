import discord, random
from discord.ext import commands
from cogs.cogfuncs import prawImage


class Subreddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def is_nsfw(self, channel):
        try:
            _gid = channel.server.id
        except AttributeError:
            return False
        data = await self.client.http.request(
            discord.http.Route(
                'GET', '/guilds/{guild_id}/channels', guild_id=_gid))
        channeldata = [d for d in data if d['id'] == channel.id][0]
        return channeldata['nsfw']

    @commands.command(pass_context=True)
    async def subreddit(self, ctx):
        async with ctx.message.channel.typing():
            commandList=str(ctx.message.content).split()

            optDict={}

            #Check if channel is NSFW
            if ctx.channel.is_nsfw():
                optDict["nsfwEnable"]=True

            #Get parameter: Subreddit
            if len(commandList) >= 2:
                if not commandList[1].startswith("-"):
                    optDict["subname"]=commandList[1]
                else:
                    optDict["subname"] = None
            else:
                optDict["subname"] = None
            
            #Get parameter: Sort by
            if "-s" in commandList: 
                if commandList.index("-s")+1<len(commandList):
                    if not commandList[commandList.index("-s")+1].startswith("-"):
                        optDict["sortby"] = commandList[commandList.index("-s")+1]                
            else:
                optDict["sortby"] = "default"

            #Get parameter: Random range
            if "-r" in commandList: 
                if commandList.index("-r")+1<len(commandList):
                    if not commandList[commandList.index("-r")+1].startswith("-"):
                        optDict["srange"] = commandList[commandList.index("-r")+1] 
            else:
                optDict["srange"] = "default"

            #Get parameter: Post type
            if "-t" in commandList: 
                if commandList.index("-t")+1<len(commandList):
                    if not commandList[commandList.index("-t")+1].startswith("-"):
                        optDict["postType"] = commandList[commandList.index("-t")+1] 
            else:
                optDict["postType"] = "default"

            print(optDict)

            embed = await prawImage.prawImgFind(**optDict)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Subreddit(client))


