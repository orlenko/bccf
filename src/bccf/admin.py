from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

from bccf.models import (Topic, TopicLink, Settings, EventForProfessionals,
    EventForParents)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']


class EventAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(EventAdmin, self).__init__(*args, **kwargs)
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


admin.site.register(Topic)
admin.site.register(TopicLink)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(EventForParents, EventAdmin)
admin.site.register(EventForProfessionals, EventAdmin)
