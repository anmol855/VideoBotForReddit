from django.shortcuts import render
import time
import BotApp.models
from BotApp.models import *
import video_creation.final_video
from subprocess import Popen
from dotenv import load_dotenv
from os import getenv, name
from reddit.subreddit import get_subreddit_threads
from utils.cleanup import cleanup
from utils.console import print_markdown, print_step
# from utils.checker import envUpdate
from video_creation.background import download_background, chop_background_video
from video_creation.final_video import make_final_video
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.voices import save_text_to_mp3
import time
import os
from plyer import notification
VERSION = 2.1
from os.path import exists
from selenium import webdriver
import time
import pyautogui



def first():
    file_exists = exists("BotMaker/data.txt")
    if(file_exists):
        os.remove("BotMaker/data.txt")
    #customspecvoices.objects.all().delete()
    print(
        """
    ██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██╗   ██╗██╗██████╗ ███████╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗    ████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
    ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ██║   ██║██║██║  ██║█████╗  ██║   ██║    ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝
    ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║    ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║███████╗██████╔╝██████╔╝██║   ██║        ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝         ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """
    )
    load_dotenv()
    # Modified by JasonLovesDoggo
    print_markdown(
        "### Thanks for using this tool! [Feel free to contribute to this project on GitHub!](https://lewismenelaws.com) If you have any questions, feel free to reach out to me on Twitter or submit a GitHub issue. You can find solutions to many common problems in the [Documentation](https://luka-hietala.gitbook.io/documentation-for-the-reddit-bot/)"
    )

    time.sleep(1)
    items=Spec.objects.all()
    items1=login.objects.all()
    #print(items[items.count()-1].MAX_COMMENT_LENGTH)
    client_id=""
    client_secret=""
    chk=CustomSpec.objects.all().count()
    l=login.objects.all()
    if(chk):
        client_id=l[l.count()-1].REDDIT_CLIENT_ID
        client_secret = l[l.count()-1].REDDIT_CLIENT_SECRET
    else:
        client_id = l[l.count()-1].REDDIT_CLIENT_ID#getenv("REDDIT_CLIENT_ID")
        client_secret = l[l.count()-1].REDDIT_CLIENT_SECRET#getenv("REDDIT_CLIENT_SECRET")

    username = items1[items1.count()-1].REDDIT_USERNAME#getenv("REDDIT_USERNAME")
    password = items1[items1.count()-1].REDDIT_PASSWORD#getenv("REDDIT_PASSWORD")
    reddit2fa = getenv("REDDIT_2FA")

def main():
    #envUpdate()
    cleanup()

    def get_obj():
        reddit_obj = get_subreddit_threads()
        return reddit_obj

    reddit_object = get_obj()
    length, number_of_comments = save_text_to_mp3(reddit_object)
    download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
    download_background()
    chop_background_video(length)
    make_final_video(number_of_comments, length)


def run_many(times):
    for x in range(times):
        x = x + 1
        print_step(
            f'on the {x}{("st" if x == 1 else ("nd" if x == 2 else ("rd" if x == 3 else "th")))} iteration of {times}'
        )  # correct 1st 2nd 3rd 4th 5th....
        main()
        Popen("cls" if name == "nt" else "clear", shell=True).wait()


def button(request):

    return render(request,'geniusvoice.html')

def output(request):
    first()
    if getenv("TIMES_TO_RUN") and isinstance(int(getenv("TIMES_TO_RUN")), int):
        run_many(int(getenv("TIMES_TO_RUN")))
    else:
        main()
    output_data = "Video Processed..!!"
    website_link = ""
    name_file=video_creation.final_video.fname()
    x=name_file
    #open text file
    text_file = open("BotMaker/data.txt", "w")
    
    #write string to file
    text_file.write(x)
    
    #close file
    text_file.close()
    text_file1 = open("BotMaker/newdata.txt", "w")
    
    #write string to file
    text_file1.write(x)
    
    #close file
    text_file1.close()
    text_file2 = open("BotMaker/datanew.txt", "w")
    
    #write string to file
    text_file2.write(x)
    
    #close file
    text_file2.close()
    print(x)
    notification.notify(
            title = "Video Ready",
            message="CheckOut on Notifications/GeneratedVideo Section" ,
           
            # displaying time
            timeout=10
        )
        # waiting time
    #time.sleep(7)
    
    print('refreshed')
    #customspecvoices.objects.all().delete()
    t=0
    #fn-call
    pyautogui.hotkey('f5')
    return render(request,"geniusvoice.html",{"output_data":output_data, "website_link":website_link,"name_file":name_file,"t":t})

