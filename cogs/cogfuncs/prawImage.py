import praw, random, os
from cogs.cogfuncs import embedGen

async def prawImgFind(subname="",sortby="hot",srange="100"):
    usableExt=["jpg","peg","png","gif"]
    usableSort=["hot","new","controversial","top","rising"]

    paramDict={}

    #Check that srange can be int
    try:
        int(srange)
    except:
        paramDict["error"] = "inappropriate_srange"
        srange = 100
    else:
        if int(srange)>500:
            paramDict["error"] = "inappropriate_srange"
            srange = 100

    if sortby not in usableSort: #if not a valid sorting method
        paramDict["error"] = "no_sort"
        sortby = "hot"

    sortby=sortby.lower()
    
    #setup reddit api connection
    reddit=praw.Reddit(client_id=os.getenv("prawClientId"), client_secret=os.getenv("prawClientSecret"), user_agent=os.getenv("prawUserAgent"))

    #If no subreddit exists with name
    if subname == None:
        paramDict["error"] = "no_sub"   
        subname = "all" 
    else:
        try:
            reddit.subreddits.search_by_name(subname, exact=True)
        except:
            paramDict["error"] = "no_sub"   
            subname = "all"              


    subGet = reddit.subreddit(subname)

    #Apply sorting method in dumb way
    if sortby=="best":
        posts = [post for post in subGet.best(limit=int(srange))]
    elif sortby=="new":
        posts = [post for post in subGet.new(limit=int(srange))]
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

    imgPosts = []
    for post in posts:
        if post.url[-3:] in usableExt:
            imgPosts.append(post)
    
    if len(imgPosts) == 0:
        paramDict["error"] = "no_image"
    else:
        submission = imgPosts[random.randint(0,len(imgPosts)-1)]

        postDictionary = {}

        paramDict["postname"] = submission.title
        paramDict["posturl"] = submission.permalink
        paramDict["imageurl"] = submission.url
        paramDict["subname"] = submission.subreddit.display_name
    
    embed = await embedGen.redditImageEmbed(**paramDict)

    return(embed)