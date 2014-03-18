from copy import deepcopy

from django.db.models import Q
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import NoReverseMatch

from embed_video.admin import AdminVideoMixin

from mezzanine.core.admin import DisplayableAdmin, DisplayableAdminForm
from mezzanine.utils.urls import admin_url
from mezzanine.conf import settings
from mezzanine.pages.admin import PageAdmin

from bccf.models import (BCCFTopic, Settings, HomeMarquee, FooterMarquee, HomeMarqueeSlide, FooterMarqueeSlide,
    PageMarquee, PageMarqueeSlide, BCCFPage, BCCFChildPage, BCCFBabyPage, BCCFGenericPage,
    Blog, Program, Article, Magazine, Video, Podcast, TipSheet, DownloadableForm, Campaign,
    Event, EventRegistration, ProgramRequest)
from bccf.settings import BCCF_CORE_PAGES
from django.core.exceptions import PermissionDenied

import logging
log = logging.getLogger(__name__)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']

class EventAttendeeInline(admin.StackedInline):
    model = EventRegistration
    fields = ('user', 'passed')

class EventAdmin(DisplayableAdmin):
    ordering = ('-created',)
    inlines = [EventAttendeeInline,]
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
                                    'price',
                                    'max_seats',
                                    'full',
                                    'bccf_topic',
                                    'image',
                                    'program',
                                    'page_for',
                                    'survey_before',
                                    'survey_after']):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['provider', 'created', 'date_start', 'date_end', 'price', 'report_link', 'attendee_link', 'full']:
                self.list_display.insert(-1, fieldname)
                
        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['provider', 'date_start', 'date_end', 'full']:
                self.list_filter.insert(-1, fieldname)

    def attendee_link(self, obj):
        return '<a href="%s">Download List of Attendees</a>' % obj.attendee_url()
    attendee_link.allow_tags = True

    def report_link(self, obj):
        return '<a href="%s">Download Report</a>' % obj.report_url()
    report_link.allow_tags = True

admin.site.register(Settings, SettingsAdmin)
admin.site.register(Event, EventAdmin)

#Pages
page_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
page_fieldsets[0][1]["fields"] += ("gparent", "page_for", "bccf_topic", "featured", "content",)

# Actions
def make_featured(modeladmin, request, queryset):
    num_rows = queryset.update(featured=True)
    if num_rows == 1:
        message_bit = "1 row featured"
    else:
        message_bit = "%s rows featured" % num_rows
make_featured.short_description = "Mark selected rows as featured"

def make_unfeatured(modeladmin, request, queryset):
    num_rows = queryset.update(featured=False)
    if num_rows == 1:
        message_bit = "1 row set as not featured"
    else:
        message_bit = "%s rows set as not featured" % num_rows
make_unfeatured.short_description = "Mark selected rows as not featured"

class BCCFTopicAdmin(DisplayableAdmin):
    ordering = ('-created',)
    def __init__(self, *args, **kwargs):
        super(BCCFTopicAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'marquee',
                                    'carousel_color']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['marquee', 'carousel_color']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['carousel_color', 'marquee']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['carousel_color', 'marquee']:
                self.list_filter.insert(-1, fieldname)
                
class BCCFBabyInlineAdmin(admin.StackedInline):
    model = BCCFBabyPage
    fk_name = "parent"
    fields = ('title', 'content', 'order',)

class BCCFGenericAdmin(DisplayableAdmin):
    ordering = ('-created',)
    inlines = (BCCFBabyInlineAdmin,)
    
    def __init__(self, *args, **kwargs):
        super(BCCFGenericAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'gparent',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)

        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'gparent', 'bccf_topic']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'gparent', 'bccf_topic']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'gparent', 'bccf_topic']:
                self.list_filter.insert(-1, fieldname)
                
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'gparent':
            q = Q() 
            for core in BCCF_CORE_PAGES:
                q  = q | Q(slug=core)
            kwargs['queryset'] = BCCFPage.objects.exclude(q)
            return db_field.formfield(**kwargs)
        return super(BCCFGenericAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class BCCFChildAdmin(DisplayableAdmin):
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('-created',)
    
    def __init__(self, *args, **kwargs):
        super(BCCFChildAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'bccf_topic']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'bccf_topic']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'bccf_topic']:
                self.list_filter.insert(-1, fieldname)

class BCCFProgramAdmin(DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('user_added', '-created',)

    def __init__(self, *args, **kwargs):
        super(BCCFProgramAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'page_for',
                                    'featured',
                                    'users',
                                    'user_added',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'bccf_topic', 'featured', 'user_added']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_filter.insert(-1, fieldname)

class BCCFResourceAdmin(DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('-created',)
    
    def __init__(self, *args, **kwargs):
        super(BCCFResourceAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'attached_document',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_filter.insert(-1, fieldname)

class BCCFPodcastResourceAdmin(DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('-created',)

    def __init__(self, *args, **kwargs):
        super(BCCFPodcastResourceAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'attached_audio',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
       # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_filter.insert(-1, fieldname)     

class BCCFVideoResourceAdmin(AdminVideoMixin, DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('-created',)
    
    def __init__(self, *args, **kwargs):
        super(BCCFVideoResourceAdmin, self).__init__(*args, **kwargs)
        
        # Fields
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'video_url',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
       # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_editable.insert(-1, fieldname)                
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_display.insert(-1, fieldname)                

        # Filter
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['page_for', 'bccf_topic', 'featured']:
                self.list_filter.insert(-1, fieldname)         
        

class BCCFTagAdmin(DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    inlines = (BCCFBabyInlineAdmin,)
    ordering = ('-created',)
    
    def __init__(self, *args, **kwargs):
        super(BCCFTagAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'user',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['featured', 'page_for', 'bccf_topic']:
                self.list_editable.insert(-1, fieldname)              
          
        # List Display      
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['featured', 'page_for', 'bccf_topic']:
                self.list_display.insert(-1, fieldname)
                
        # Filters
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['featured', 'page_for']:
                self.list_filter.insert(-1, fieldname)

admin.site.register(BCCFPage, PageAdmin)
admin.site.register(BCCFTopic, BCCFTopicAdmin)
admin.site.register(BCCFGenericPage, BCCFGenericAdmin)
admin.site.register(Blog, BCCFChildAdmin)
admin.site.register(Program, BCCFProgramAdmin)
admin.site.register(Campaign, BCCFTagAdmin)
admin.site.register(Article, BCCFResourceAdmin)
admin.site.register(DownloadableForm, BCCFResourceAdmin)
admin.site.register(Magazine, BCCFResourceAdmin)
admin.site.register(TipSheet, BCCFResourceAdmin)

admin.site.register(Podcast, BCCFPodcastResourceAdmin)
admin.site.register(Video, BCCFVideoResourceAdmin)

# Program Request
class ProgramRequestAdmin(admin.ModelAdmin):
    actions = ['accept_requests']
    fields = ('title', 'comment', 'user', 'accept', 'accepted_on', 'created')
    readonly_fields = ('created', 'accepted_on')
    list_display = ['title', 'user', 'accept', 'accepted_on', 'created']
    list_filter = ('accept', 'created')
    ordering = ('-created',)
    
    def accept_requests(self, request, queryset):
        for row in queryset:
            row.accept_request()
        num_rows = queryset.update(accept=True)
        if num_rows == 1:
            return '%s Request Accepted.'% num_rows
        else:
            return '%s Requests Accepted.' % num_rows    
    accept_requests.short_description = 'Accept Selected Requests'
    
admin.site.register(ProgramRequest, ProgramRequestAdmin)

#Inline
class HomeMarqueeInline(admin.TabularInline):
    model = HomeMarqueeSlide.marquee.through  # @UndefinedVariable

class FooterMarqueeInline(admin.TabularInline):
    model = FooterMarqueeSlide.marquee.through  # @UndefinedVariable

class PageMarqueeInline(admin.TabularInline):
    model = PageMarqueeSlide.marquee.through  # @UndefinedVariable

#Marquees
class MarqueeSlideAdmin(admin.ModelAdmin):
    fields = ('title', 'caption', 'url', 'linkLabel', 'image')
    list_display = ['title', 'caption', 'url']

class HomeMarqueeSlideAdmin(MarqueeSlideAdmin):
    inlines = [HomeMarqueeInline]

class FooterMarqueeSlideAdmin(admin.ModelAdmin):
    fields = ('title', 'caption', 'image')
    inlines = [FooterMarqueeInline]
    list_display = ['title', 'caption']

class PageMarqueeSlideAdmin(MarqueeSlideAdmin):
    inlines = [PageMarqueeInline]

class MarqueeAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_filter = ('active',)

admin.site.register(HomeMarqueeSlide, HomeMarqueeSlideAdmin)
admin.site.register(FooterMarqueeSlide, FooterMarqueeSlideAdmin)
admin.site.register(PageMarqueeSlide, PageMarqueeSlideAdmin)
admin.site.register(HomeMarquee, MarqueeAdmin)
admin.site.register(FooterMarquee, MarqueeAdmin)
admin.site.register(PageMarquee)
