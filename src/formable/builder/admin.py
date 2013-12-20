from copy import deepcopy

from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
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
        ('Form Details', {'fields':['title', 'type', 'structure']}),
        ('Meta', {'fields':['created']})
    ]
    inlines = [
        FormPublishedLine
    ]
    list_display = ('title', 'id', 'type', 'created')
    list_filter = ['type', 'created']
    search_fields = ['title', 'id', 'type']
    
class FormPublishedAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(FormPublishedAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['title',
                                    'gparent',
                                    'image',]):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
    
class FormFilledAdmin(admin.ModelAdmin):
    """
    Admin for FormFilled
    """
    readonly_fields = ('filled',)
    fieldsets = [
        ('Form Details', {'fields':['title', 'form_published', 'user']}),
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
