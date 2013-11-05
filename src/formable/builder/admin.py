from django.contrib import admin
from formable.builder.models import FormStructure, FormFilled, Question, FieldAnswer

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

class FormStructureAdmin(admin.ModelAdmin):
    """
    Admin form for FormStructure.
    """
    fieldsets = [
        ('Form Details', {'fields':['title', 'type', 'structure']})
    ]
    inlines = [
        FormFilledLine, QuestionLine
    ]
    list_display = ('title', 'id', 'type', 'created')
    list_filter = ['type', 'created']
    search_fields = ['title', 'id', 'type']
    
class FormFilledAdmin(admin.ModelAdmin):
    """
    Admin for FormFilled
    """
    fieldsets = [
        ('Form Details', {'fields':['form_structure', 'user']})
    ]
    inlines = [
        FieldAnswerLine
    ]
    list_display = ('form_structure', 'user', 'filled')
    list_filter = ['form_structure', 'user', 'filled']
    search_fields = ['form_structure', 'user']

class QuestionAdmin(admin.ModelAdmin):
    """
    Admin for Question
    """
    fieldsets = [
        ('Question Details', {'fields':['question']}),
        ('Question Owners', {'fields':['form_structure', 'form_filled']})
    ]
    inlines = [
        FieldAnswerLine
    ]
    list_display = ('question', 'form_structure', 'form_filled', 'date')
    list_filter = ['form_structure', 'form_filled', 'date']
    search_fields = ['question', 'form_structure', 'form_filled']
    
class FieldAnswerAdmin(admin.ModelAdmin):
    """
    Admin for field answer.
    """
    fieldsets = [
        ('Field Answer Details', {'fields':['answer']}),
        ('Field Answer Owners', {'fields':['question', 'form_filled']})
    ]
    list_display = ('answer', 'question', 'form_filled', 'answered')
    list_filter = ['question', 'form_filled', 'answered']
    search_fields = ['answer', 'question', 'form_filled']

admin.site.register(FormStructure, FormStructureAdmin)
admin.site.register(FormFilled, FormFilledAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FieldAnswer, FieldAnswerAdmin)
