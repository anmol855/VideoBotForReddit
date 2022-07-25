import re
from os import getenv, environ

import praw
import BotApp.models
from BotApp.models import *
from utils.console import print_step, print_substep
from utils.subreddit import get_subreddit_undone
from utils.videos import check_done
from praw.models import MoreComments

TEXT_WHITELIST = set("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890")


def textify(text):
    return "".join(filter(TEXT_WHITELIST.__contains__, text))


def try_env(param, backup):
    try:
        return environ[param]
    except KeyError:
        return backup


def get_subreddit_threads():
    """
    Returns a list of threads from the AskReddit subreddit.
    """
    global submission
    print_substep("Logging into Reddit.")

    content = {}
    if str(getenv("REDDIT_2FA")).casefold() == "yes":
        print("\nEnter your two-factor authentication code from your authenticator app.\n")
        code = input("> ")
        print()
        pw = getenv("REDDIT_PASSWORD")
        passkey = f"{pw}:{code}"
    else:
        items1=login.objects.all()
        passkey = items1[items1.count()-1].REDDIT_PASSWORD
        #passkey = getenv("REDDIT_PASSWORD")
    items=Spec.objects.all()
    items1=login.objects.all()
    chk=CustomSpec.objects.all().count()
    client_id1=""
    client_secret1=""
    loginobj=login.objects.all()
    if(chk):
        l=CustomSpec.objects.all()
        client_id1=loginobj[loginobj.count()-1].REDDIT_CLIENT_ID
        client_secret1 = loginobj[loginobj.count()-1].REDDIT_CLIENT_SECRET
    else:
        client_id1=loginobj[loginobj.count()-1].REDDIT_CLIENT_ID
        client_secret1=loginobj[loginobj.count()-1].REDDIT_CLIENT_SECRET
    reddit = praw.Reddit(
        client_id=client_id1,#getenv("REDDIT_CLIENT_ID"),
        client_secret=client_secret1,#getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing Reddit threads",
        username=items1[items1.count()-1].REDDIT_USERNAME,#getenv("REDDIT_USERNAME"),
        passkey=passkey,
        check_for_async=False,
    )
    subreddit = items[items.count()-1].SUBREDDIT#reddit.subreddit("askreddit")
    print_substep("Subreddit not defined. Using AskReddit.")
    """
	Ask user for subreddit input
	"""
    print_step("Getting subreddit threads...")
    #f not getenv(
     #   "SUBREDDIT"
    #)  # note to user. you can have multiple subreddits via reddit.subreddit("redditdev+learnpython")
        #try:
            #subreddit = reddit.subreddit(
                #re.sub(r"r\/", "", input("What subreddit would you like to pull from? "))
                # removes the r/ from the input
            #)
       # except ValueError:

    #else:
    print_substep(f"Using subreddit: r/{items[items.count()-1].SUBREDDIT} from environment variable config")
    subreddit = reddit.subreddit(
            items[items.count()-1].SUBREDDIT
            #getenv("SUBREDDIT")
        )  # Allows you to specify in .env. Done for automation purposes.

    #fetching post via url
    sp=CustomSpec.objects.all()
    url=""
    postid=""
    if(sp.count()):
        url=sp[sp.count()-1].POST_URL
        x=url.find('comments/')
        y=url.find('/',x+8)
        z=url.find('/',y+5)
        print(url[x+9:z])
        postid=url[x+9:z]
    if postid:
        submission = reddit.submission(id=postid)
        print('submission',submission)
        #print(submission.comments.body)
    else:
        if items[items.count()-1].FilterType=='Hot':
            threads = subreddit.hot(limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='New':
            threads = subreddit.new(limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top':
            threads = subreddit.top(limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-Now':
            threads = subreddit.top("hour",limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-Today':
            threads = subreddit.top("day",limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-ThisWeek':
            threads = subreddit.top("week",limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-ThisMonth':
            threads = subreddit.top("month",limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-ThisYear':
            threads = subreddit.top("year",limit=25)#post options #day #hour #week #month #year #all
        if items[items.count()-1].FilterType=='Top-AllTime':
            threads = subreddit.top("all",limit=25)#post options #day #hour #week #month #year #all
        submission = get_subreddit_undone(threads, subreddit)
    submission = check_done(submission)  # double checking
    if submission is None:
        return get_subreddit_threads()  # submission already done. rerun
    upvotes = submission.score
    ratio = submission.upvote_ratio * 100
    num_comments = submission.num_comments

    print_substep(f"Video will be: {submission.title} :thumbsup:", style="bold green")
    print_substep(f"Thread has {upvotes} upvotes", style="bold blue")
    print_substep(f"Thread has a upvote ratio of {ratio}%", style="bold blue")
    print_substep(f"Thread has {num_comments} comments", style="bold blue")
    environ["VIDEO_TITLE"] = str(textify(submission.title))  # todo use global instend of env vars
    environ["VIDEO_ID"] = str(textify(submission.id))

    content["thread_url"] = f"https://reddit.com{submission.permalink}"
    content["thread_title"] = submission.title
    # content["thread_content"] = submission.content
    content["comments"] = []
    chk=CustomSpec.objects.all().count()
    comlen=0
    if(chk):
        l=CustomSpec.objects.all()
        comlen=l[l.count()-1].MAX_COMMENT_LENGTH
    else:
        comlen=items[items.count()-1].MAX_COMMENT_LENGTH
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        if top_level_comment.body in ["[removed]", "[deleted]"]:
            continue  # # see https://github.com/JasonLovesDoggo/RedditVideoMakerBot/issues/78
        if not top_level_comment.stickied:
            if len(top_level_comment.body) <=comlen:#int(try_env("MAX_COMMENT_LENGTH", 500)):
                content["comments"].append(
                    {
                        "comment_body": top_level_comment.body,
                        "comment_url": top_level_comment.permalink,
                        "comment_id": top_level_comment.id,
                    }
                )
    print_substep("Received subreddit threads Successfully.", style="bold green")
    return content
