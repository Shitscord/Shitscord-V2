import discord, praw, textwrap

#Generate embed message for a fatal error such as no content found at all.
async def errorEmbed(errorList):
    if "none_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="No content could be found using the given parameters. Try a different subreddit, increase the range, or try a different type.")
    elif "only_nsfw_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="Only content marked as NSFW could be found. You may be trying to access an NSFW subreddit in a SFW channel. Either try a SFW subreddit or repeat the command in an NSFW channel.")

#Generate string of errors when a non fatal error occurs, such as incorrect type or sorting option
async def embedStatus(errorList):
    errorMessage = ":warning:"
    if "inappropriate_srange" in errorList:
        errorMessage += "`-r was not an integer between 1 and 500. Using default of 100.` "
    if "no_sort" in errorList:
        errorMessage += "`Invalid -s sorting option. Using default of hot.` "
    if "no_sub_provided" in errorList:
        errorMessage += "`No subreddit provided. Using default of r/all.` "
    if "no_sub_found" in errorList:
        errorMessage += "`No accessible subreddit found by that name. Using default of r/all.` "
    if "no_type" in errorList:
        errorMessage += "`Invalid type chosen. Using default of any.`"
    return(errorMessage)

#Handle embed generation for image posts
async def imageEmbed(errorList, postname="", posturl="", imageurl="", subname="", content="", icon=""):
    print("Error: ", errorList)
    posturl = "http://www.reddit.com" + str(posturl)
    suburl = "http://www.reddit.com/r/" + subname
    subname = "r/" + subname
    embed = discord.Embed(title=postname, colour=discord.Colour(0xff4500), url=posturl)
    embed.set_image(url=content)
    if icon == "":
        icon = "https://i.imgur.com/dsf46oW.png"
    embed.set_author(name=subname, url=suburl, icon_url=icon)
    if len(errorList) != 0:
        embed.description = embedStatus(errorList)
    return(embed)

#Handle embed generation for text posts
async def textEmbed(errorList, postname="", posturl="", imageurl="", subname="", content="", icon=""):
    print("Error: ", errorList)
    posturl = "http://www.reddit.com" + str(posturl)
    suburl = "http://www.reddit.com/r/" + subname
    subname = "r/" + subname
    embed = discord.Embed(title=postname, colour=discord.Colour(0xff4500), url=posturl)
    if len(content) > 1000:
        splitList = []
        for line in textwrap.wrap(content, 1000):
            splitList.append(line)
        content = splitList
        x=0
        for string in content:
            embed.add_field(name=str(x+1)+" of "+str(len(content)), value=string)
            x+=1
    else:
        embed.add_field(name="1 of 1", value=content)
    if icon == "":
        icon = "https://i.imgur.com/dsf46oW.png"
    embed.set_author(name=subname, url=suburl, icon_url=icon)
    if len(errorList) != 0:
        embed.description = embedStatus(errorList)
    return(embed)