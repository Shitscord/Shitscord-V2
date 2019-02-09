import praw, random

async def prawImgFind(prawDepInj,subreddit="all",sortby="top",srange="100",retries="3"):
    reddit=praw.Reddit(client_id=prawDepInj.clientId, client_secret=prawDepInj.clientSecret, user_agent=prawDepInj.userAgent)
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except:
        return(1)    

    subGet = reddit.subreddit(subreddit)
    posts = [post for post in subGet.hot(limit=int(srange))]
    randTop = min(len(posts),int(srange))

    usableExt=["jpg","peg","png","gif"]

    for i in range(0,int(retries)):
        randomPost = posts[random.randint(0,randTop)].url
        print(randomPost)
        if randomPost[-3:] in usableExt:
            return(randomPost)
        i+=1
    return(2)