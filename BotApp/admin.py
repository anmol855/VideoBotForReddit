from django.contrib import admin
from . models import *
from django.db import models

# Register your models here.
admin.site.register(Spec)
admin.site.register(login)
admin.site.register(CustomSpec)
admin.site.register(voices)
admin.site.register(customspecvoices)