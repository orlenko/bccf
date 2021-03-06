# -*- coding: utf-8
from copy import deepcopy

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse

from bccf.admin import make_featured, make_unfeatured
from mezzanine.core.admin import DisplayableAdmin

from pybb.models import Category, Forum, Topic, Post, Profile, Attachment, PollAnswer

from pybb import util
username_field = util.get_username_field()


class ForumInlineAdmin(admin.TabularInline):
    model = Forum
    fields = ['name', 'hidden', 'position']
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'hidden', 'forum_count']
    list_per_page = 20
    ordering = ['position']
    search_fields = ['name']
    list_editable = ['position']

    inlines = [ForumInlineAdmin]


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'hidden', 'position', 'topic_count', ]
    list_per_page = 20
    raw_id_fields = ['moderators']
    ordering = ['-category']
    search_fields = ['name', 'category__name']
    list_editable = ['position', 'hidden']
    fieldsets = (
        (None, {
                'fields': ('category', 'name', 'hidden', 'position', )
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields': ('updated', 'description', 'headline', 'post_count', 'moderators')
                }
            ),
        )


class PollAnswerAdmin(admin.TabularInline):
    model = PollAnswer
    fields = ['text', ]
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'forum', 'created', 'head', 'post_count', 'poll_type',]
    list_per_page = 20
    raw_id_fields = ['user', 'subscribers']
    ordering = ['-created']
    date_hierarchy = 'created'
    search_fields = ['name']
    fieldsets = (
        (None, {
                'fields': ('forum', 'name', 'user', ('created', 'updated'), 'poll_type',)
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields': (('views', 'post_count'), ('sticky', 'closed'), 'subscribers')
                }
         ),
        )
    inlines = [PollAnswerAdmin, ]
    
class BCCFTopicAdmin(DisplayableAdmin):
    actions = [make_featured, make_unfeatured]
    list_per_page = 20
    raw_id_fields = ['user', 'subscribers']
    ordering = ['-created']
    date_hierarchy = 'created'
    search_fields = ['name']
    def __init__(self, *args, **kwargs):
        super(BCCFTopicAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['forum',
                                    'name',
                                    'user',
                                    'closed',
                                    'content',
                                    'bccf_topic',
                                    'featured',
                                    'image',
                                    'page_for']):
                self.fieldsets[0][1]['fields'].insert(3, field)     
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['head', 'post_count', 'featured']:
                self.list_display.insert(-1, fieldname)
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['featured']:
                self.list_filter.insert(-1, fieldname)

class TopicReadTrackerAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'time_stamp']
    search_fields = ['user__%s' % username_field]

class ForumReadTrackerAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'time_stamp']
    search_fields = ['user__%s' % username_field]

class PostAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'created', 'updated', 'on_moderation', 'summary']
    list_editable = ['on_moderation']
    list_per_page = 20
    actions = ['make_approve', 'make_unapprove']
    raw_id_fields = ['user', 'topic']
    ordering = ['-created']
    date_hierarchy = 'created'
    search_fields = ['body']
    fieldsets = (
        (None, {
                'fields': ('topic', 'user')
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields' : (('created', 'updated'), 'user_ip')
                }
         ),
        (_('Message'), {
                'fields': ('body', 'body_html', 'body_text', 'on_moderation')
                }
         ),
        )
        
    def make_approve(self, request, queryset):
        num_rows = queryset.update(on_moderation=False)
        if num_rows == 1:
            message_bit = '1 post approved'
        else:
            message_bit = '%s posts approved' % num_rows
    make_approve.short_description = "Approve selected posts"
    
    def make_unapprove(self, request, queryset):
        num_rows = queryset.update(on_moderation=True)
        if num_rows == 1:
            message_bit = '1 post disapproved'
        else:
            message_bit = '%s posts disapproved' % num_rows
    make_unapprove.short_description = "Disapprove selected posts"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'time_zone', 'language', 'post_count']
    list_per_page = 20
    ordering = ['-user']
    search_fields = ['user__%s' % username_field]
    fieldsets = (
        (None, {
                'fields': ('user', 'time_zone', 'language')
                }
         ),
        (_('Additional options'), {
                'classes': ('collapse',),
                'fields' : ('avatar', 'signature', 'show_signatures')
                }
         ),
        )


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file', 'size', 'admin_view_post', 'admin_edit_post']

    def admin_view_post(self, obj):
        return u'<a href="%s">view</a>' % obj.post.get_absolute_url()
    admin_view_post.allow_tags = True
    admin_view_post.short_description = _('View post')

    def admin_edit_post(self, obj):
        return u'<a href="%s">edit</a>' % reverse('admin:pybb_post_change', args=[obj.post.pk])
    admin_edit_post.allow_tags = True
    admin_edit_post.short_description = _('Edit post')


#admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, BCCFTopicAdmin)
admin.site.register(Post, PostAdmin)
#admin.site.register(Attachment, AttachmentAdmin)

if util.get_pybb_profile_model() == Profile:
    admin.site.register(Profile, ProfileAdmin)

# This can be used to debug read/unread trackers

#admin.site.register(TopicReadTracker, TopicReadTrackerAdmin)
#admin.site.register(ForumReadTracker, ForumReadTrackerAdmin)