from django.contrib import admin
from formable.builder.models import FormStructure

class FormStructureAdmin(admin.ModelAdmin):
    """
    Admin form for FormStructure.
    """
    fieldsets = [
        ('Form Details', {'fields':['form_title', 'form_structure_type', 'form_structure']}),
    ]
    list_display = ('form_title', 'form_structure_type', 'id', 'created')

admin.site.register(FormStructure, FormStructureAdmin)
