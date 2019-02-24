import discord, praw

async def redditImageEmbed(postname="", posturl="", imageurl="", subname="", error=None):
    print("Error: "+str(error))
    if error=="no_image":
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="No images could be found. Try a different subreddit or increase -s. You may also be trying to access an NSFW subreddit in a SFW channel")
    else:
        posturl = "http://www.reddit.com" + str(posturl)
        suburl = "http://www.reddit.com/r/" + subname
        subname = "r/" + subname
        embed = discord.Embed(title=postname, colour=discord.Colour(0xff4500), url=posturl)
        embed.set_image(url=imageurl)
        embed.set_author(name=subname, url=suburl, icon_url="https://i.imgur.com/dsf46oW.png")
        if error != None:
            if error == "inappropriate_srange":
                errorMessage = ":warning:` -s was not an integer between 1 and 500. Using default of 100.`"
            if error == "no_sort":
                errorMessage = ":warning:` Invalid sorting option. Using default of hot.`"
            if error == "no_sub":
                errorMessage = ":warning:` Invalid or no subreddit provided. Using default of r/all.`"
            embed.description = errorMessage
    return(embed)