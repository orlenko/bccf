from django import forms
from django.db.models import Sum
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.comments.forms import CommentSecurityForm

from mezzanine.conf import settings
from mezzanine.generic.models import Rating

import logging
import json
from bccf.models import UserProfile, EventForParents, EventForProfessionals
from formable.builder.forms import FormStructureForm
from formable.builder.models import FormStructure, FormPublished, Question
log = logging.getLogger(__name__)

class RatingRenderer(RadioFieldRenderer):
    def render(self):
        """
        Creates a rating-friendly list of radiobuttons
        """
        return(mark_safe(u''.join([u'%s' % force_unicode(w.tag()) for w in self])))

class BCCFRatingForm(CommentSecurityForm):
    """
    Form for a rating. Subclasses ``CommentSecurityForm`` to make use
    of its easy setup for generic relations.
    """
    value = forms.ChoiceField(label='', widget=forms.RadioSelect(attrs={'class': 'star'}, renderer=RatingRenderer),
                              choices=zip(*(settings.RATINGS_RANGE,) * 2))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BCCFRatingForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Check unauthenticated user's cookie as a light check to
        prevent duplicate votes.
        """
        bits = (self.data["content_type"], self.data["object_pk"])
        self.current = "%s.%s" % bits
        request = self.request
        self.previous = request.COOKIES.get("mezzanine-rating", "").split(",")
        already_rated = self.current in self.previous
        if already_rated and not self.request.user.is_authenticated():
            raise forms.ValidationError(_("Already rated."))
        return self.cleaned_data

    def save(self):
        """
        Saves a new rating - authenticated users can update the
        value if they've previously rated.
        """
        user = self.request.user
        rating_value = self.cleaned_data["value"]
        rating_name = self.target_object.get_ratingfield_name()
        rating_manager = getattr(self.target_object, rating_name)
        if user.is_authenticated():
            try:
                rating_instance = rating_manager.get(user=user)
            except Rating.DoesNotExist:
                rating_instance = Rating(user=user, value=rating_value)
                rating_manager.add(rating_instance)
                self.target_object.rating_count = self.target_object.rating_count + 1
            else:
                if rating_instance.value != int(rating_value):
                    rating_instance.value = rating_value
                    rating_instance.save()
        else:
            rating_instance = Rating(value=rating_value)
            rating_manager.add(rating_instance)    
            # edits
        
        sum = Rating.objects.filter(object_pk=self.target_object.pk).aggregate(Sum('value'))
        self.target_object.rating_sum = int(sum['value__sum'])
        self.target_object.rating_average = self.target_object.rating_sum / self.target_object.rating_count
        self.target_object.save()
        return rating_instance

class ProfileForm(forms.ModelForm):
    class Meta:
        exclude = ('membership_order',)
        model = UserProfile

class ParentEventForm(forms.ModelForm):
    class Meta:
        model = EventForParents
        fields = ('title', 'content', 'provider', 'price', 'location_city',
            'location_street', 'location_street2', 'location_postal_code',
            'date_start', 'date_end')
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'}),
            'date_end': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'})
        }

##################
# For Wizard

class ProfessionalEventForm(forms.ModelForm):
    """
    Form for creating a Professional Event using the Wizard
    """
    #image = forms.ImageField();
    class Meta:
        model = EventForProfessionals
        fields = ('title', 'content', 'provider', 'price', 'location_city',
            'location_street', 'location_street2', 'location_postal_code',
            'date_start', 'date_end', 'image', 'bccf_topic')
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'}),
            'date_end': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'})
        }
            
    def __init__(self, *args, **kwargs):
        super(ProfessionalEventForm, self).__init__(*args, **kwargs)
        self.fields['survey'] = forms.BooleanField(label='Create Surveys?',
            widget=forms.CheckboxInput, required=False)
    def save(self, **kwargs):
        data = self.cleaned_data
        if 'survey' in data: # check and remove the survey key-value pair
            del data['survey']
        if 'bccf_topic' in data:
            topics = data['bccf_topic']
            del data['bccf_topic']
        event = EventForProfessionals(**data)
        event.save()
        for topic in topics:
            event.bccf_topic.add(topic)
        return event
        
            
class FormStructureSurveyBase(forms.Form):
    class Meta:
        abstract = True            
    def save(self, user):    
        data = self.cleaned_data
        if 'clone' in data: # check and remove the clone key-value pair
            del data['clone']
        if 'after_survey' in data: # check and remove the after_survey key-value pair
            del data['after_survey']
        form_struct = FormStructure.objects.create(structure=data['structure'], title=data['title'])
        published = FormPublished.objects.create(form_structure=form_struct, user=user)

        # Create Questions based on structure
        struct = json.loads(form_struct.structure)
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
                        form_published=published, required=required,
                        num_answers=num_answers)
                    question.save()
        # End Create Questions
        return published # FormPublished object            
            
class FormStructureSurveyFormOne(FormStructureSurveyBase):
    """
    Form for creating a before survey in the Professional Event creation Wizard
    """
    title = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_title'}))
    structure = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_data'}))
    type = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_type'}))
    after_survey = forms.BooleanField(label='Create After Survey?',
        widget=forms.CheckboxInput, required=False)
    clone = forms.BooleanField(label='Use this Survey as template?',
        widget=forms.CheckboxInput, required=False)

class FormStructureSurveyFormTwo(FormStructureSurveyBase):
    """
    Form for creating an after survey in the Professional Event creation Wizard.
    """
    title = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_title'}))
    structure = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_data'}))
    type = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'form_structure_type'}))