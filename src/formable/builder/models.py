from django.db import models
from django.forms import ModelForm

class FormStructure(models.Model):
    """
    Model for the form structure. The form structure can be stored as JSON, HTML,
    YAML, or XML.
    """
    FORM_TYPE = (
        ('JSON', 'JSON'),
        #('HTML', 'HTML'), # To be Implemented
        #('YAML', 'YAML'), # To be Implemented
        #('XML', 'XML'), # To be Implemented
    )

    form_title = models.CharField("Form Title", max_length=100)
    form_structure = models.TextField("Form Sturcture")
    form_structure_type = models.CharField("Form Type", max_length=4, choices=FORM_TYPE)
    created = models.DateTimeField(auto_now_add=True)
