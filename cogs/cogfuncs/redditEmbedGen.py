import discord, praw, textwrap, numpy
from skimage import io

#Generate embed message for a fatal error such as no content found at all.
async def errorEmbed(errorList):
    print("Generating error embed:", errorList)
    if "fatal_none_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="No content could be found using the given parameters. Try a different subreddit, increase the range, or try a different type.")
    elif "fatal_only_nsfw_found" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="Only content marked as NSFW could be found. You may be trying to access an NSFW subreddit in a SFW channel. Either try a SFW subreddit or repeat the command in an NSFW channel.")
    elif "fatal_private_or_quarantined" in errorList:
        embed = discord.Embed(title=":warning: Error", colour=discord.Colour(0xd00202), description="This subreddit has been Quarantined, Private, or does not exist.")
    return(embed)

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

#Choose a color for the embed based on the subreddits icon
async def colorGenerator(icon_url):
    img = io.imread(icon_url)
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0).tolist()
    avg_color = [int(x) for x in avg_color][:3]
    hexcode = int('%02x%02x%02x' % tuple(avg_color), 16)
    return(hexcode)

#Handle embed generation for image posts
async def imageEmbed(contDict):
    print("Error: ", contDict["errorlist"])
    fullurl = "http://www.reddit.com" + str(contDict["posturl"])
    suburl = "http://www.reddit.com/r/" + contDict["subname"]
    fullsubname = "r/" + contDict["subname"]
    if contDict["icon"] == "":
        contDict["icon"] = "https://i.imgur.com/dsf46oW.png"
    embed = discord.Embed(title=contDict["postname"], colour=discord.Colour(await colorGenerator(contDict["icon"])), url=fullurl)
    embed.set_image(url=contDict["content"])
    embed.set_author(name=fullsubname, url=suburl, icon_url=contDict["icon"])
    if len(contDict["errorlist"]) != 0:
        embed.description = await embedStatus(contDict["errorlist"])
    return(embed)

#Handle embed generation for text posts
async def textEmbed(contDict):
    print("Error: ", contDict["errorlist"])
    fullurl = "http://www.reddit.com" + str(contDict["posturl"])
    suburl = "http://www.reddit.com/r/" + contDict["subname"]
    fullsubname = "r/" + contDict["subname"]
    if contDict["icon"] == "":
        contDict["icon"] = "https://i.imgur.com/dsf46oW.png"
    embed = discord.Embed(title=contDict["postname"], colour=discord.Colour(await colorGenerator(contDict["icon"])), url=fullurl)
    content = contDict["content"]
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
    embed.set_author(name=fullsubname, url=suburl, icon_url=contDict["icon"])
    if len(contDict["errorlist"]) != 0:
        embed.description = await embedStatus(contDict["errorlist"])
    return(embed)