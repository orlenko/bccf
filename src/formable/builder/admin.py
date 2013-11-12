from django.contrib import admin
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
    
class FormPublishedAdmin(admin.ModelAdmin):
    """
    Admin for FormPublished
    """
    readonly_fields = ('form_structure', 'published',)
    fieldsets = [
        ('Published Form Details', {'fields':['title', 'user', 'form_structure']}),
        ('Meta', {'fields':['published']})
    ]
    inlines = [
        QuestionLine
    ]
    list_display = ('title', 'form_structure', 'id', 'user', 'published')
    list_filter = ['form_structure', 'user', 'published']
    search_fields = ['title', 'form_structure', 'id', 'user']
    
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
        ('Question Details', {'fields':['question']}),
        ('Question Owners', {'fields':['form_published']}),
        ('Meta', {'fields':['date']})
    ]
    inlines = [
        FieldAnswerLine
    ]
    list_display = ('question', 'form_published', 'date')
    list_filter = ['form_published', 'date']
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
