import logging

from django import forms
from django.contrib.contenttypes.models import ContentType

from form_utils.forms import BetterForm

from formable.builder.models import FormStructure

from bccf.models import BCCFTopic

log = logging.getLogger(__name__)


class FormStructureForm(forms.ModelForm):
    """
    Form for creating a new form structure.
    """
    PAGE_FOR = (
        ('parent', 'Parents'),
        ('professional', 'Professionals')    
    )    
    title = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_title'}))
    structure = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_data'}))
    type = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_type'}))
    content = forms.CharField(widget=forms.Textarea)
    page_for = forms.ChoiceField(choices=PAGE_FOR)
    bccf_topic = forms.ModelMultipleChoiceField(queryset=BCCFTopic.objects.all().order_by('title'))

    class Meta:
        model = FormStructure
        fields = ['title', 'structure', 'type']


class ListForPublishForm(forms.Form):
    """
    Form for creating a select field consisting the available structures for publishing
    """

    def __init__(self, *args, **kwargs):
        super(ListForPublishForm, self).__init__(*args, **kwargs)
        self.struct_id = forms.ChoiceField(FormStructure.objects.all().values_list('id', 'title'))


class CloneFormForm(forms.Form):
    """
    Creates a dropdown containing the created form structures
    """
    def __init__(self, *args, **kwargs):
        super(CloneFormForm, self).__init__(*args, **kwargs)
        self.form_structure = forms.ChoiceField(FormStructure.objects.all().values_list('id', 'title'))


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
