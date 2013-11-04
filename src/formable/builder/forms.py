import logging

from django import forms
from form_utils.forms import BetterForm

from formable.builder.models import FormStructure

log = logging.getLogger(__name__)

class CloneFormForm(BetterForm):
    """
    Creates a dropdown containing the created form structures
    """
    records = FormStructure.objects.all()
    titles = records.values_list('id','form_title')
    form_structures = forms.ChoiceField(titles)
    
    class Meta:
        fieldsets = [('main', {'fields':['form_structures'], 'legend':'Test'})]
  
class ViewFormForm(BetterForm):
    """
    Creates a form based on the saved form structure. Parses the JSON and creates
    a new form structure that can be rendered by Django.
    """
    base_fieldsets = None
        
    def __init__(self, fieldsets, fields, *args, **kwargs):
        self.base_fieldsets = fieldsets
        super(ViewFormForm, self).__init__(*args, **kwargs)
        self.fields = fields
