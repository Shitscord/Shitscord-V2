import discord, praw

async def redditImageEmbed(postname, posturl, imageurl, subname):
    posturl = "http://www.reddit.com" + str(posturl)
    suburl = "http://www.reddit.com/r/" + subname
    subname = "r/" + subname

    print(postname)
    print(posturl)
    print(imageurl)
    print(subname)
    print(suburl)

    embed = discord.Embed(title=postname, colour=discord.Colour(0xff4500), url=posturl)
    embed.set_image(url=imageurl)
    embed.set_author(name=subname, url=suburl, icon_url="https://i.imgur.com/dsf46oW.png")
    return(embed)