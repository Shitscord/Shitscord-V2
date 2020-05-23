import discord, praw

async def redditImageEmbed(errorList, postType = "", postname="", posturl="", imageurl="", subname=""):
    print("Error: ", errorList)
    if "none_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="No images could be found using the given parameters. Try a different subreddit or increase -r.")
    elif "only_nsfw_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="Only content marked as NSFW could be found. You may be trying to access an NSFW subreddit in a SFW channel. Either try a SFW subreddit or repeat the command in an NSFW channel.")
    else:
        posturl = "http://www.reddit.com" + str(posturl)
        suburl = "http://www.reddit.com/r/" + subname
        subname = "r/" + subname
        embed = discord.Embed(title=postname, colour=discord.Colour(0xff4500), url=posturl)
        embed.set_image(url=imageurl)
        embed.set_author(name=subname, url=suburl, icon_url="https://i.imgur.com/dsf46oW.png")
        if len(errorList) != 0:
            errorMessage = ":warning:"
            if "inappropriate_srange" in errorList:
                errorMessage += "`-r was not an integer between 1 and 500. Using default of 100.` "
            if "no_sort" in errorList:
                errorMessage += "`Invalid -s sorting option. Using default of hot.` "
            if "no_sub_provided" in errorList:
                errorMessage += "`No subreddit provided. Using default of r/all.` "
            if "no_sub_found" in errorList:
                errorMessage += "`No accessible subreddit found by that name. Using default of r/all.` "
            embed.description = errorMessage
    return(embed)