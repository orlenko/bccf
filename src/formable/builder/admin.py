from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from bccf.admin import make_featured, make_unfeatured
from formable.builder.models import FormStructure, FormPublished, FormFilled, Question, FieldAnswer

class FormFilledLine(admin.TabularInline):
    """
    Inline for FormFilled.
    """
    model = FormFilled
    
class QuestionLine(admin.TabularInline):
    """
    Inline for Question.
    """
    model = Question
    
class FieldAnswerLine(admin.TabularInline):
    """
    Inline for FieldAnswer
    """
    model = FieldAnswer
    
class FormPublishedLine(admin.TabularInline):
    """
    Inline for FormPublished
    """
    model = FormPublished

class FormStructureAdmin(admin.ModelAdmin):
    """
    Admin form for FormStructure.
    """
    readonly_fields = ('created',)
    fieldsets = [
        ('Form Details', {'fields':['title', 'user', 'type', 'structure']}),
        ('Meta', {'fields':['created']})
    ]
    inlines = [
        FormPublishedLine
    ]
    list_display = ('title', 'user', 'id', 'type', 'created', 'clone_link', 'edit_link', 'publish_link')
    list_filter = ['type', 'user', 'created']
    search_fields = ['title', 'id', 'type']
    
    def clone_link(self, obj):
        return '<a href="%s" target="_blank">Clone Form</a>' % obj.get_clone_url()
    clone_link.allow_tags = True
    def edit_link(self, obj):
        return '<a href="%s" target="_blank">Edit Form</a>' % obj.get_edit_url()
    edit_link.allow_tags = True
    def publish_link(self, obj):
        return '<a href="%s" target="_blank">Publish Form</a>' % obj.get_publish_url()
    publish_link.allow_tags = True
        
class FormPublishedAdmin(DisplayableAdmin):
    actions = ['make_closed', 'make_open', make_featured, make_unfeatured]
    
    def __init__(self, *args, **kwargs):
        super(FormPublishedAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['title',
                                    'content',
                                    'closed',
                                    'page_for',
                                    'bccf_topic',
                                    'featured',
                                    'image',]):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
        # Editable in the list display
        if self.list_editable == DisplayableAdmin.list_editable:
            self.list_editable = list(deepcopy(self.list_editable))
            for fieldname in ['closed', 'featured']:
                self.list_editable.insert(-1, fieldname)
                
        # Fields in the list display
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['featured', 'closed', 'report_link']:
                self.list_display.insert(-1, fieldname)
                
        # Filters
        if self.list_filter == DisplayableAdmin.list_filter:
            self.list_filter = list(deepcopy(self.list_filter))
            for fieldname in ['featured', 'gparent', 'closed']:
                self.list_filter.insert(-1, fieldname)
            
        # Actions
        #if self.actions == DisplayableAdmin.actions:
        #    self.actions = list(deepcopy(self.actions))
        #    for action in ['make_closed', 'make_open']:
        #        self.actions.insert(-1, action)          
            
    def report_link(self, obj):
        return '<a href="%s">Download Report</a>' % obj.get_report_url()
    report_link.allow_tags = True
    
    def make_closed(self, request, queryset):
        num_rows = queryset.update(closed=True)
        if num_rows == 1:
            message_bit = "1 form closed"
        else:
            message_bit = "%s forms closed" % num_rows
    make_closed.short_description = "Mark selected forms as close"
    
    def make_open(self, request, queryset):
        num_rows = queryset.update(closed=False)
        if num_rows == 1:
            message_bit = "1 form opened"
        else:
            message_bit = "%s forms opened" % num_rows
    make_open.short_description = "Mark selected forms as open"  
    
class FormFilledAdmin(admin.ModelAdmin):
    """
    Admin for FormFilled
    """
    readonly_fields = ('filled', 'title', 'form_published',)
    fieldsets = [
        ('Form Details', {'fields':['user', 'title', 'form_published']}),
        ('Meta', {'fields':['filled']})
    ]
    inlines = [
        FieldAnswerLine
    ]
    list_display = ('title', 'form_published', 'user', 'filled')
    list_filter = ['form_published', 'user', 'filled']
    search_fields = ['title','form_published', 'user']

class QuestionAdmin(admin.ModelAdmin):
    """
    Admin for Question
    """
    readonly_fields = ('date',)
    fieldsets = [
        ('Question Details', {'fields':['question', 'num_answers', 'required']}),
        ('Question Owners', {'fields':['form_published']}),
        ('Meta', {'fields':['date']})
    ]
    inlines = [
        FieldAnswerLine
    ]
    list_display = ('question', 'form_published', 'date')
    list_filter = ['form_published', 'date', 'required']
    search_fields = ['question', 'form_published']
    
class FieldAnswerAdmin(admin.ModelAdmin):
    """
    Admin for field answer.
    """
    readonly_fields = ('answered',)
    fieldsets = [
        ('Field Answer Details', {'fields':['answer']}),
        ('Field Answer Owners', {'fields':['question', 'form_filled']}),
        ('Meta', {'fields':['answered']})
    ]
    list_display = ('answer', 'question', 'form_filled', 'answered')
    list_filter = ['question', 'form_filled', 'answered']
    search_fields = ['answer', 'question', 'form_filled']

admin.site.register(FormStructure, FormStructureAdmin)
admin.site.register(FormPublished, FormPublishedAdmin)
admin.site.register(FormFilled, FormFilledAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FieldAnswer, FieldAnswerAdmin)
