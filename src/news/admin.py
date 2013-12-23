from copy import deepcopy

from django.contrib import admin
from bccf.admin import BCCFPageAdmin

from .models import NewsPost

admin.site.register(NewsPost)