import logging
import json

from django import forms
from django.contrib.contenttypes.models import ContentType
from mezzanine.utils.models import upload_to

from form_utils.forms import BetterForm
from formable.builder.models import FormStructure, FormPublished, Question
from bccf.models import BCCFTopic
from bccf.settings import MEDIA_ROOT

log = logging.getLogger(__name__)


class FormStructureForm(forms.Form):
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
    image = forms.ImageField()
    featured = forms.BooleanField();

    class Meta:
        model = FormStructure
        fields = ['title', 'structure', 'type']
        
    def is_valid(self):        
        if not self.data['content']:
            return False
        return True
        
    def handle_upload(self):
        image_path = 'uploads/childpage/'+self.files['image'].name
        destination = open(MEDIA_ROOT+'/'+image_path, 'wb+')
        for chunk in self.files['image'].chunks():
            destination.write(chunk)
        destination.close()
        return image_path

    def save(self, user, **kwargs):
        form_structure = FormStructure.objects.create(structure=self.data['structure'], title=self.data['title'])
        form_published = FormPublished.objects.create(form_structure=form_structure, user=user, content=self.data['content'], 
            page_for=self.data['page_for'], featured=self.data['featured'])
        if 'bccf_topic' in self.data:
            form_published.bccf_topic = bccf_topic=self.data['bccf_topic']
            form_published.save()
        if 'image' in self.files:
            form_published.image = self.handle_upload()
            form_published.save()
    
        # Create Questions based on structure
        struct = json.loads(form_structure.structure)
        for fieldset in struct["fieldset"]:
            for field in fieldset["fields"]:
               if "label" in field: # don't save static text
                    if "required" in field["attr"]:
                        required = 0
                    else:
                        required = 1
                    num_answers = 0
                    if field['class'] == 'multiselect-field' or field['class'] == 'checkbox-field':
                        num_answers = len(field["options"])
    
                    question = Question(question=field["label"],
                        form_published=form_published, required=required,
                        num_answers=num_answers)
                    question.save()
        return form_published
        
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
