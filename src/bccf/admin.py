from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

from bccf.models import (Topic, TopicLink, Settings, EventForProfessionals,
    EventForParents, Article, Magazine, TipSheet, DownloadableForm, Video)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']


class ParentsEventAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(ParentsEventAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'provider',
                                    'date_start',
                                    'date_end',
                                    'location_city',
                                    'location_street',
                                    'location_street2',
                                    'location_postal_code',
                                    'price']):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['provider', 'date_start', 'date_end', 'price']:
                self.list_display.insert(-1, fieldname)
                
class ProfessionalsEventAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(ProfessionalsEventAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'provider',
                                    'date_start',
                                    'date_end',
                                    'location_city',
                                    'location_street',
                                    'location_street2',
                                    'location_postal_code',
                                    'price',
                                    'survey_before',
                                    'survey_after']):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['provider', 'date_start', 'date_end', 'price']:
                self.list_display.insert(-1, fieldname)


admin.site.register(Topic)
admin.site.register(TopicLink)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(EventForParents, ParentsEventAdmin)
admin.site.register(EventForProfessionals, ProfessionalsEventAdmin)
admin.site.register(Article)
admin.site.register(Magazine)
admin.site.register(TipSheet)
admin.site.register(DownloadableForm)
admin.site.register(Video)
