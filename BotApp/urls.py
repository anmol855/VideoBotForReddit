from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('videos', views.videos, name='videos'),
    path('videosgen', views.videosgen, name='videosgen'),
    path('download',views.download,name='download'),
    path('', views.signin, name="signin"),
    path('profile', views.profile, name="profile"),
    path('currentprofile',views.currentprofile,name="currentprofile"),
    path('processedvideo',views.processedvideo,name='processedvideo'),
    path('updateprofile',views.updateprofile,name='updateprofile'),
    path('home',views.home,name='home'),
    path('landingpage',views.landingpage,name='landingpage'),
    path('test',views.test,name='test'),
    path('customindex',views.customindex,name='customindex'),
    path('voices',views.voices,name='voices'),
    path('subredditvoices',views.subredditvoices,name='subredditvoices'),
    path('availtracks',views.availtracks,name='availtracks')
]