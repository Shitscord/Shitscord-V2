import praw, random, os

async def prawImgFind(subreddit="all",sortby="hot",srange="100"):
    usableExt=["jpg","peg","png","gif"]
    usableSort=["hot","new","controversial","top","rising"]
    #Check that srange can be int
    try:
        float(srange)
    except ValueError:
        return("srange_not_int")

    if sortby not in usableSort: #if not a valid sorting method
        return("no_sort")

    sortby=sortby.lower()
    
    #setup reddit api connection
    reddit=praw.Reddit(client_id=os.getenv("prawClientId"), client_secret=os.getenv("prawClientSecret"), user_agent=os.getenv("prawUserAgent"))

    #If no subreddit exists with name
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except:
        return("no_sub")    

    subGet = reddit.subreddit(subreddit)

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
        return("no_image")
    else:
        randomPost = imgPosts[random.randint(0,len(imgPosts)-1)]
        randomPostUrl = randomPost.url
        return(randomPostUrl)