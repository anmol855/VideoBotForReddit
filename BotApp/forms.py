from django import forms
from django.forms import ModelForm
from .models import Spec,login,CustomSpec,voices,customspecvoices


voicechosen=""
class SpecForm(ModelForm):
	class Meta:
		model = Spec
		fields = ('SUBREDDIT', 'MAX_COMMENT_LENGTH','BACKGROUND_VIDEO_URL','SELECTED_VOICE','FilterType')
		labels = {
			'REDDIT_CLIENT_ID': 'REDDIT_CLIENT_ID',
			'REDDIT_CLIENT_SECRET': 'REDDIT_CLIENT_SECRET',
			'SUBREDDIT': 'SUBREDDIT',
			'MAX_COMMENT_LENGTH': 'MAX_COMMENT_LENGTH',
			'FilterType':'FilterType',
			'BACKGROUND_VIDEO_URL':'BACKGROUND_VIDEO_URL',
			'SELECTED_VOICE':'SELECTED_VOICE',		
		}
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
		widgets = {
			'SUBREDDIT': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter'}),
			'MAX_COMMENT_LENGTH': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter'}),
			#'POST_URL':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter'}),
			#'FilterType':forms.ChoiceField(choices =FILTER),
			'BACKGROUND_VIDEO_URL':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter'}),
			'SELECTED_VOICE':forms.TextInput(attrs={'class':'form-control',}),
		}
	
	def __init__(self, *args, **kwargs):
		super(SpecForm, self).__init__(*args, **kwargs)
		x=voices.objects.all()
		voicechosen=x[x.count()-1].FilterType
		print('voicechosen',voicechosen)
		self.fields["SELECTED_VOICE"].initial =voicechosen

class LoginForm(ModelForm):
	class Meta:
		model = login
		fields = ('REDDIT_USERNAME', 'REDDIT_PASSWORD','REDDIT_CLIENT_ID','REDDIT_CLIENT_SECRET')
		labels = {
			'REDDIT_USERNAME': '',
			'REDDIT_PASSWORD': '',	
			'REDDIT_CLIENT_ID':'',
			'REDDIT_CLIENT_SECRET':'',	
		}
		widgets = {
			'REDDIT_USERNAME': forms.TextInput(attrs={'class':'form-control', 'placeholder':'REDDIT-USERNAME'}),
			'REDDIT_PASSWORD': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'REDDIT-PASSWORD'}),
			'REDDIT_CLIENT_ID': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'REDDIT_CLIENT_ID'}),
			'REDDIT_CLIENT_SECRET': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'REDDIT_CLIENT_SECRET'}),
		}


class CustomSpecForm(ModelForm):
	class Meta:
		model = CustomSpec
		fields = ('MAX_COMMENT_LENGTH','POST_URL','BACKGROUND_VIDEO_URL','SELECTED_VOICE')
		labels = {
			'MAX_COMMENT_LENGTH': 'MAX_COMMENT_LENGTH',
			'POST_URL':'POST_URL',
			'BACKGROUND_VIDEO_URL':'BACKGROUND_VIDEO_URL',	
		}
		widgets = {
			'MAX_COMMENT_LENGTH': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter'}),
			'POST_URL':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter'}),
			'BACKGROUND_VIDEO_URL':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter'}),
			'SELECTED_VOICE':forms.TextInput(attrs={'class':'form-control',}),
		}
	def __init__(self, *args, **kwargs):
		super(CustomSpecForm, self).__init__(*args, **kwargs)
		x=customspecvoices.objects.all()
		voicechosen=x[x.count()-1].FilterType
		print('voicechosen',voicechosen)
		self.fields["SELECTED_VOICE"].initial =voicechosen

class VoiceForm(ModelForm):
	class Meta:
		model = voices
		fields = ('FilterType',)
		labels = {
			'FilterType':'FilterType'		
		}

class CustomVoiceForm(ModelForm):
	class Meta:
		model = customspecvoices
		fields = ('FilterType',)
		labels = {
			'FilterType':'FilterType'		
		}