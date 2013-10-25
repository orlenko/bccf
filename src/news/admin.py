from copy import deepcopy

from django.contrib import admin
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.pages.admin import PageAdmin

from .models import NewsPost


common_fieldsets = deepcopy(PageAdmin.fieldsets)
common_fieldsets[0][1]['fields'].append('content')


class NewsAdmin(DisplayableAdmin):
    fieldsets = common_fieldsets

    def in_menu(self):
        for (_name, items) in settings.ADMIN_MENU_ORDER:
            if "news.NewsPost" in items:
                return True
        return False


admin.site.register(NewsPost, NewsAdmin)
