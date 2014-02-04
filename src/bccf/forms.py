import logging
import json

from django import forms
from django.db.models import Sum
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.comments.forms import CommentSecurityForm

#from ckeditor.widgets import CKEditorWidget
from tinymce.widgets import TinyMCE

from mezzanine.conf import settings
from mezzanine.generic.models import Rating

from bccf.models import UserProfile, EventForParents, EventForProfessionals,\
    Settings
from bccf.settings import MEDIA_ROOT

from formable.builder.models import FormStructure, FormPublished, Question
from django.contrib.auth.models import User
from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.urls import slugify, unique_slug, admin_url
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from mezzanine.utils.email import send_mail_template


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
            raise forms.ValidationError("Already rated.")
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

        summ = Rating.objects.filter(object_pk=self.target_object.pk).aggregate(Sum('value'))  # @UndefinedVariable - poor PyDev
        self.target_object.rating_sum = int(summ['value__sum'])
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
    image = forms.ImageField()
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))#CKEditorWidget())
    class Meta:
        model = EventForProfessionals
        fields = ('title', 'content', 'provider', 'price', 'location_city',
            'location_street', 'location_street2', 'location_postal_code',
            'date_start', 'date_end', 'bccf_topic')
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'}),
            'date_end': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'})
        }

    def __init__(self, *args, **kwargs):
        super(ProfessionalEventForm, self).__init__(*args, **kwargs)
        self.fields['survey'] = forms.BooleanField(label='Create Surveys?',
            widget=forms.CheckboxInput, required=False)


    def handle_upload(self):
        image_path = 'uploads/childpage/'+self.files['0-image'].name
        destination = open(MEDIA_ROOT+'/'+image_path, 'wb+')
        for chunk in self.files['0-image'].chunks():
            destination.write(chunk)
        destination.close()
        return image_path

    def save(self, **kwargs):
        data = self.cleaned_data
        if 'survey' in data: # check and remove the survey key-value pair
            del data['survey']
        if 'bccf_topic' in data:
            topics = data['bccf_topic']
            del data['bccf_topic']
        if 'image' in data:
            del data['image']
        event = EventForProfessionals(**data)
        if '0-image' in self.files:
            event.image = self.handle_upload()

        event.save()
        for topic in topics:
            event.bccf_topic.add(topic)
        return event


class FormStructureSurveyBase(forms.Form):
    """
    Superclass that creates a generic save function for the wizard forms.
    """
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


class ProfileFieldsForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            exclude = settings.ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS + ['user', 'description', 'photo']
            widgets = {'organization': forms.HiddenInput()}


class AddUserForm(Html5Mixin, forms.ModelForm):
    '''This form is used by an organization user.
    '''
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        exclude = settings.ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS + ['description', 'photo']
        widgets = {'organization': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = User._meta.get_all_field_names()  # @UndefinedVariable PyDev limitation ("_meta")
        try:
            self.fields["username"].help_text = "Only letters, numbers, dashes or underscores please"
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
        # Add any profile fields to the form.
        profile_fields = ProfileFieldsForm().fields
        self.fields.update(profile_fields)


    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError("Username can only contain letters, "
                                          "numbers, dashes or underscores.")
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)  # @UndefinedVariable PyDev limitation ("exclude")
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("This username is already registered")

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append("Passwords do not match")
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append("Password must be at least %s characters" %
                              settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)  # @UndefinedVariable PyDev limitation ("exclude")
        if len(qs) == 0:
            return email
        raise forms.ValidationError("This email is already registered")

    def save(self, *args, **kwargs):
        kwargs["commit"] = False
        user = super(AddUserForm, self).save(*args, **kwargs)
        try:
            self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                username = "%(first_name)s %(last_name)s" % self.cleaned_data
                if not username.strip():
                    username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)  # @UndefinedVariable PyDev limitation ("exclude")
                user.username = unique_slug(qs, "username", slugify(username))
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        user.save()

        # Save profile model.
        ProfileFieldsForm(self.data, self.files, instance=user.profile).save()
        settings.use_editable()
        if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
            settings.ACCOUNTS_APPROVAL_REQUIRED):
            user.is_active = False
            user.save()
        return user


class AddExistingUserForm(forms.Form):
    organization = forms.IntegerField(widget=forms.HiddenInput())
    user = forms.TypedChoiceField(coerce=int)

    def __init__(self, *args, **kwargs):
        super(AddExistingUserForm, self).__init__(*args, **kwargs)
        organization = self.initial.get('organization', self.data.get('organization'))
        self.fields['user'].choices=[
            (rec.pk, rec.get_full_name())
            for rec in User.objects.filter(
                profile__organization=None,
                profile__membership_type='professional'
            ).exclude(pk=organization)  # @UndefinedVariable PyDev does not get it
        ]

    def save(self, *args, **kwargs):
        user = User.objects.get(pk=self.cleaned_data['user'])
        log.debug('Saving user %s with org %s' % (user, self.cleaned_data['organization']))
        profile = user.profile
        profile.organization_id = self.cleaned_data['organization']
        profile.save()


class AddUsersForm(forms.Form):
    organization = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, request):
        organization = User.objects.get(pk=self.data['organization'])
        users = {}
        errors = {}
        email_validator = EmailValidator(message='Email is not valid')
        for k, v in self.data.items():
            if not ('-' in k):
                continue
            kind, index = k.split('-')
            user = users.setdefault(index, {})
            if kind == 'email':
                try:
                    email_validator(v)
                except ValidationError, err:
                    log.debug('Failed to validate %s' % v, exc_info=1)
                    errors.setdefault(index, [v]).append(err.message)
                    users.pop(index, None)
            user[kind] = v
        for index, user in users.items():
            if user['email']:
                email = user['email'].strip()
                # Make sure this user does not already exist
                try:
                    _existing = User.objects.get(username__iexact=email)
                except User.DoesNotExist:
                    pass
                else:
                    log.debug('Duplicate user %s' % email)
                    errors.setdefault(index, [email]).append('This user already exists.')
                    users.pop(index, None)
                    continue

                rec = User.objects.create(email=email,
                                          username=email,
                                          first_name=user.get('first_name', 'Firstname'),
                                          last_name=user.get('last_name', 'Lastname'),
                                          is_active=False)
                send_mail_template('BCCF Invitation from %s (%s)' % (organization.get_full_name(), organization.email),
                                   'bccf/email/membership_invitation_to_organization',
                                   Settings.get_setting('SERVER_EMAIL'),
                                   email,
                                   context={
                                        'user': rec,
                                        'organization': organization,
                                        'link': ('http://%s%s' % (request.get_host(),
                                                                  admin_url(rec.__class__, "change", rec.id)))
                                   },
                                   attachments=None,
                                   fail_silently=settings.DEBUG,
                                   addr_bcc=None)
            else:
                pass
                #errors.setdefault(index, [' '.join(user.values())]).append('Email is required')
        log.debug('Returning users, errors: %s %s' % (users, errors))
        return users, errors


class DelMember(forms.Form):
    user = forms.IntegerField()

    def save(self):
        user = User.objects.get(pk=self.cleaned_data['user'])
        profile = user.profile
        profile.organization = None
        profile.save()
        log.debug('User %s organization is now %s' % (user, profile.organization))