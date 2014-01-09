from copy import deepcopy

from django.contrib import admin
from bccf.admin import BCCFChildAdmin

from .models import NewsPost

admin.site.register(NewsPost, BCCFChildAdmin)