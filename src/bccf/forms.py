from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.comments.forms import CommentSecurityForm

from mezzanine.conf import settings
from mezzanine.generic.models import Rating

import logging
from bccf.models import UserProfile, EventForProfessionals
from formable.builder.forms import FormStructureForm
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
            else:
                if rating_instance.value != int(rating_value):
                    rating_instance.value = rating_value
                    rating_instance.save()
        else:
            rating_instance = Rating(value=rating_value)
            rating_manager.add(rating_instance)
        return rating_instance


class ProfileForm(forms.ModelForm):
    class Meta:
        exclude = ('membership_order',)
        model = UserProfile
        
class ProfessionalEventForm(forms.Form):
    """
    Form for creating a Professional Event using the Wizard
    """
    def __init__(self, *args, **kwargs):
        super(ProfessionalEventForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(label='Title', 
            widget=forms.TextInput(attrs={'required':''}), required=True)
        self.fields['content'] = forms.CharField(label='Event Description',
            widget=forms.Textarea(attrs={'class':'mceEditor'}), required=True)
        self.fields['date_start'] = forms.CharField(label='Event Start (Date Time):',
            widget=forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM', 'required':''}),
            required=True)
        self.fields['date_end'] = forms.CharField(label='Event End (Date Time):',
            widget=forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM', 'required':''}),
            required=True)
        self.fields['location_city'] = forms.CharField(label='City', required=False)
        self.fields['location_street'] = forms.CharField(label='Street', required=False)
        self.fields['location_street2'] = forms.CharField(label='Street (line2)', required=False)
        self.fields['location_postal_code'] = forms.CharField(label='Postal Code', required=False)
        self.fields['price'] = forms.CharField(label='Price($)',
            widget=forms.TextInput(attrs={'required':''}), required=True)
        self.fields['survey'] = forms.BooleanField(label='Create Surveys?',
            widget=forms.CheckboxInput, required=False)
            
class FormStructureSurveyFormOne(FormStructureForm):
    """
    Form for creating a before survey in the Professional Event creation Wizard
    
    It is a child class of FormStructureForm found in formable.builder.forms
    """
    after_survey = forms.BooleanField(label='Create After Survey?',
        widget=forms.CheckboxInput, required=False)
    clone = forms.BooleanField(label='Clone this Structure?',
        widget=forms.CheckboxInput, required=False)
       
class FormStructureSurveyFormTwo(FormStructureForm):
    """
    Form for creating an after survey in the Professional Event creation Wizard.
    
    It is a child class of FormStructureForm found in formable.builder.forms
    """
