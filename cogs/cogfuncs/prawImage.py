import praw, random, os
import cogs.cogfuncs.embedGen as embedGen

async def prawImgFind(subname="",sortby="",srange="",postType="",nsfwEnable=False):
    #Setup image types, sorting methods, empty dictionary for parameters, and list for errors to be reported
    usableExt=["jpg","peg","png","gif"]
    usableSort=["hot","new","controversial","top","rising"]
    usableType=["image"]
    errorList = []
    paramDict={}
    paramDict["postType"] = postType

    #Check that srange can be int
    if srange == "default":
        srange = 50
    else:
        try:
            int(srange)
        except:
            errorList.append("inappropriate_srange")
            srange = 50
        else:
            if int(srange)>500:
                errorList.append("inappropriate_srange")
                srange = 50

    #Check that sortby is a valid option
    sortby=sortby.lower()
    if sortby == "default":
        sortby = "hot"
    else:
        if sortby not in usableSort: #if not a valid sorting method
            errorList.append("no_sort")
            sortby = "hot"

    #Check that postType is a valid option
    postType=postType.lower()
    if postType == "default":
        postType = "image"
    else:
        if postType not in usableType:
            errorList.append("noType")

    #setup reddit api connection
    reddit=praw.Reddit(client_id=os.getenv("prawClientId"), client_secret=os.getenv("prawClientSecret"), user_agent=os.getenv("prawUserAgent"))

    #If no subreddit name provided or sub name is invalid, use r/all and return error
    if subname == None:
        errorList.append("no_sub_provided")   
        subname = "all" 
    else:
        try:
            reddit.subreddits.search_by_name(subname, exact=True)
        except:
            errorList.append("no_sub_found")   
            subname = "all"              

    subGet = reddit.subreddit(subname)

    #Apply sorting method in dumb way
    if sortby=="best":
        posts = [post for post in subGet.best(limit=int(srange))]
    elif sortby=="new":
        posts = [post for post in subGet.new(limit=int(srange))]
    elif sortby=="controversial":
        posts = [post for post in subGet.controversial(limit=int(srange))]
    elif sortby=="top":
        posts = [post for post in subGet.top(limit=int(srange))]
    elif sortby=="rising":
        posts = [post for post in subGet.rising(limit=int(srange))]
    elif sortby=="hot":
        posts = [post for post in subGet.hot(limit=int(srange))]

    #Create a list of all images, skip NSFW images if requesting channel is not NSFW
    imgPosts = []
    nsfwFound = False
    for post in posts:
        if post.url[-3:] in usableExt:
            if nsfwEnable:
                imgPosts.append(post)
            else:
                nsfwFound = True
                if not post.over_18:
                    imgPosts.append(post)

    if len(imgPosts) == 0 and nsfwFound == True and nsfwEnable == False:
        errorList.append("only_nsfw_found")
    elif len(imgPosts) == 0 and nsfwFound == False:
        errorList.append("none_found")
    else:
        submission = imgPosts[random.randint(0,len(imgPosts)-1)]
        paramDict["postname"] = submission.title
        paramDict["posturl"] = submission.permalink
        paramDict["imageurl"] = submission.url
        paramDict["subname"] = submission.subreddit.display_name
    
    embed = await embedGen.redditImageEmbed(errorList, **paramDict)

    return(embed)