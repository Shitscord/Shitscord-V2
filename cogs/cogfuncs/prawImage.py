import praw, random, os
import cogs.cogfuncs.redditEmbedGen as redditEmbedGen


 
async def prawImgFind(subname="",sortby="",srange="",postType="",nsfwEnable=False):
    #Setup image types, sorting methods, empty dictionary for parameters, and list for errors to be reported
    usableExt=["jpg","peg","png","gif"]
    usableSort=["hot","new","controversial","top","rising"]
    usableType=["image", "text", "all"]
    errorList = []
    paramDict={}
    
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
        postType = "all"
    else:
        if postType not in usableType:
            errorList.append("no_type")
            postType = "all"
    
    #setup reddit api connection
    reddit=praw.Reddit(client_id=os.getenv("prawClientId"), client_secret=os.getenv("prawClientSecret"), user_agent=os.getenv("prawUserAgent"), check_for_async=False)

    #If no subreddit name provided or sub name is invalid, use r/all and return error
    if subname == "default":
        errorList.append("no_sub_provided")   
        subname = "all" 
    else:
        try:
            reddit.subreddits.search_by_name(subname, exact=True)
        except:
            errorList.append("no_sub_found")   
            subname = "all"              
    print(errorList)
    print(subname)
    subGet = reddit.subreddit(subname)
    try:
        subStatus = subGet.subreddit_type
    except:
        subStatus = None

    if subStatus == "public" or subname == "all":
        print("publicsub")
        try:
            paramDict["icon"] = subGet.icon_img
        except:
            paramDict["icon"] = ""
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
        txtPosts = []
        imgPosts = []
        nsfwimgFound = False
        nsfwtxtFound = False
        for post in posts:
            if post.url[-3:] in usableExt:
                if nsfwEnable:
                    imgPosts.append(post)
                else:
                    if not post.over_18:
                        imgPosts.append(post)
                    else:
                        nsfwimgFound = True
            else:
                if post.selftext != "":
                    if nsfwEnable:
                        txtPosts.append(post)
                    else:
                        if not post.over_18:
                            txtPosts.append(post)
                        else:
                            nsfwtxtFound = True

        if len(imgPosts) == 0 and nsfwimgFound == True and nsfwEnable == False and postType=="image": #If seeking sfw img and only found nsfw
            errorList.append("fatal_only_nsfw_found")
        elif len(imgPosts) == 0 and nsfwimgFound == False and postType=="image": #If no images found at all
            errorList.append("fatal_none_found")
        elif len(txtPosts) == 0 and nsfwtxtFound == True and nsfwEnable == False and postType=="text" or len(txtPosts) == 0 and nsfwtxtFound == True and nsfwEnable == False and postType=="all": #If seeking sfw txt and only found nsfw
            errorList.append("fatal_only_nsfw_found")
        elif len(txtPosts) == 0 and nsfwtxtFound == False and postType=="text": #If no text found at all
            errorList.append("fatal_none_found")
        elif len(txtPosts) == 0 and len(imgPosts) == 0 and postType == "all": #If nothing found for all
            errorList.append("fatal_none_found")
        elif len(imgPosts) == 0 and len(txtPosts) ==0 and nsfwimgFound == True and nsfwEnable == False and postType=="all":
            errorList.append("fatal_only_nsfw_found")
        elif len(imgPosts) == 0 and len(txtPosts) == 0 and nsfwimgFound == False and postType=="all":
            errorList.append("fatal_none_found")
        else:
            if postType == "image":
                submission = imgPosts[random.randint(0,len(imgPosts)-1)]
                paramDict["postname"] = submission.title
                paramDict["posturl"] = submission.permalink
                paramDict["content"] = submission.url
                paramDict["subname"] = submission.subreddit.display_name
                paramDict["type"] = "image"
            elif postType == "text":
                submission = txtPosts[random.randint(0,len(txtPosts)-1)]
                paramDict["postname"] = submission.title
                paramDict["posturl"] = submission.permalink
                paramDict["content"] = submission.selftext
                paramDict["subname"] = submission.subreddit.display_name
                paramDict["type"] = "text"
            elif postType == "all":
                fullList = txtPosts + imgPosts
                submission = fullList[random.randint(0,len(fullList)-1)]
                paramDict["postname"] = submission.title
                paramDict["posturl"] = submission.permalink
                paramDict["subname"] = submission.subreddit.display_name
                if submission.url[-3:] in usableExt:
                    paramDict["type"] = "image"
                    paramDict["content"] = submission.url
                else:
                    paramDict["type"] = "text"
                    paramDict["content"] = submission.selftext
        paramDict["errorlist"] = errorList

    else:
        paramDict["errorlist"] = ["fatal_private_or_quarantined"]    

    return(paramDict)