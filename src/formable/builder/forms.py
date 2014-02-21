import logging
import json

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from ckeditor.widgets import CKEditor
#from filebrowser.fields import FileBrowseFormField, FileBrowseWidget

from mezzanine.utils.models import upload_to

from form_utils.forms import BetterForm
from formable.builder.models import FormStructure, FormPublished, Question
from bccf.models import BCCFTopic
from bccf.settings import MEDIA_ROOT

log = logging.getLogger(__name__)


class FormStructureForm(forms.ModelForm):
    """
    Form form Creating from structures
    """
    structure = forms.CharField(widget=forms.HiddenInput(attrs={'id':'form_structure_data'}))

    class Meta:
        model = FormStructure
        fields = ['title', 'structure']

class FormPublishForm(forms.Form):
    """
    Form for creating a new form structure.
    """
    PAGE_FOR = (
        ('parent', 'Parents'),
        ('professional', 'Professionals')
    )
    title = forms.CharField()
    content = forms.CharField(widget=CKEditor)
    page_for = forms.ChoiceField(choices=PAGE_FOR)
    bccf_topic = forms.ModelMultipleChoiceField(queryset=BCCFTopic.objects.all().order_by('title'))
    image = forms.ImageField()#FileBrowseFormField(widget=FileBrowseWidget)
    featured = forms.BooleanField()

    def is_valid(self):
        if not self.data['title']:
            return False
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

    def save(self, struct, user, **kwargs):
        form_published = FormPublished.objects.create(form_structure=struct, user=user, title=self.data['title'], content=self.data['content'])
        if 'page_for' in self.data:
            form_published.page_for = self.data['page_for']
        if 'featured' in self.data:
            form_published.featured = self.data['featured']
        if 'bccf_topic' in self.data:
            form_published.bccf_topic = bccf_topic=self.data['bccf_topic']
        if 'image' in self.files:
            form_published.image = self.handle_upload()
        form_published.save()

        # Create Questions based on structure
        struct = json.loads(struct.structure)
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

class CloneFormForm(forms.Form):
    """
    Creates a dropdown containing the created form structures
    """
    def __init__(self, user, *args, **kwargs):
        super(CloneFormForm, self).__init__(*args, **kwargs)
        self.form_structure = forms.ChoiceField(FormStructure.objects.filter(Q(user=None) | Q(user=user)).order_by('user').values_list('id', 'title'))


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
