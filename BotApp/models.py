from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#from BotApp.views import page
class Spec(models.Model):#Venue
	#REDDIT_CLIENT_ID = models.CharField(max_length=200)
	#REDDIT_CLIENT_SECRET = models.CharField(max_length=300)
	#REDDIT_USERNAME = models.CharField( max_length=115)
	#REDDIT_PASSWORD = models.CharField(max_length=300)
	SUBREDDIT = models.CharField( max_length=115)
	MAX_COMMENT_LENGTH = models.IntegerField()
	#POST_URL=models.URLField(max_length=500,blank=True)
	FILTER=(
        ('Hot', 'Hot'),
        ('New', 'New'),
        #('Top', 'Top'),
        ('Top-Now', 'Top-Now'),
        ('Top-Today', 'Top-Today'),
        ('Top-ThisWeek', 'Top-ThisWeek'),
        ('Top-ThisMonth', 'Top-ThisMonth'),
		('Top-ThisYear', 'Top-ThisYear'),
		('Top-AllTime', 'Top-AllTime'),
    	)
	FilterType=models.CharField(max_length=60,choices=FILTER)
	BACKGROUND_VIDEO_URL=models.URLField(max_length=500,blank=True)
	SELECTED_VOICE=models.CharField(max_length=115)
class CustomSpec(models.Model):#Venue
	#REDDIT_CLIENT_ID = models.CharField(max_length=200)
	#REDDIT_CLIENT_SECRET = models.CharField(max_length=300)
	MAX_COMMENT_LENGTH = models.IntegerField()
	POST_URL=models.URLField(max_length=500,blank=True)
	flag=models.IntegerField(default = 0)
	BACKGROUND_VIDEO_URL=models.URLField(max_length=500,blank=True)
	SELECTED_VOICE=models.CharField(max_length=115)
class login(models.Model):
	REDDIT_USERNAME = models.CharField( max_length=115)
	REDDIT_PASSWORD = models.CharField(max_length=300)
	REDDIT_CLIENT_ID = models.CharField(max_length=200,default="")
	REDDIT_CLIENT_SECRET = models.CharField(max_length=300,default="")
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return self.REDDIT_USERNAME

class Blog(models.Model):
    created = models.DateTimeField(auto_now_add=True)

class voices(models.Model):
	#available_voices=models.CharField(max_length=115)
	FILTER=(
        ('Brian', 'Brian (English, British)'),
        ('Amy', 'Amy (English, British)'),
        ('Emma', 'Emma (English, British)'),
        ('Geraint', 'Geraint (English, Welsh)'),
        ('Russell', 'Russell (English, Australian)'),
        ('Nicole', 'Nicole (English, Australian)'),
        ('Joey', 'Joey (English, American)'),
		('Justin', 'Justin (English, American)'),
		('Matthew', 'Matthew (English, American)'),
		('Ivy', 'Ivy (English, American) '),
		('Joanna', 'Joanna (English, American) '),
		('Kendra', 'Kendra (English, American)'),
		('Kimberly', 'Kimberly (English, American)'),
		('Salli', 'Salli (English, American)'),
		('Raveena', 'Raveena (English, Indian) '),
		('Aditi', 'Aditi (+English) (Hindi)'),
    	)
	FilterType=models.CharField(max_length=360,choices=FILTER)

class customspecvoices(models.Model):
	#=models.CharField(max_length=115)
	FILTER=(
        ('Brian', 'Brian (English, British)'),
        ('Amy', 'Amy (English, British)'),
        ('Emma', 'Emma (English, British)'),
        ('Geraint', 'Geraint (English, Welsh)'),
        ('Russell', 'Russell (English, Australian)'),
        ('Nicole', 'Nicole (English, Australian)'),
        ('Joey', 'Joey (English, American)'),
		('Justin', 'Justin (English, American)'),
		('Matthew', 'Matthew (English, American)'),
		('Ivy', 'Ivy (English, American) '),
		('Joanna', 'Joanna (English, American) '),
		('Kendra', 'Kendra (English, American)'),
		('Kimberly', 'Kimberly (English, American)'),
		('Salli', 'Salli (English, American)'),
		('Raveena', 'Raveena (English, Indian) '),
		('Aditi', 'Aditi (+English) (Hindi)'),
    	)
	FilterType=models.CharField(max_length=360,choices=FILTER)
