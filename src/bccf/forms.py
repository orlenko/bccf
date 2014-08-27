import logging
import json

from django import forms
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.comments.forms import CommentSecurityForm
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from mezzanine.core.forms import Html5Mixin
from mezzanine.utils.urls import slugify, unique_slug, admin_url
from mezzanine.utils.email import send_mail_template
from mezzanine.conf import settings
from mezzanine.generic.models import Rating

from bccf.models import UserProfile, Event, Settings, ProgramRequest, Program, Campaign
from bccf.settings import MEDIA_ROOT
from bccf.widgets import AdvancedFileInput

from formable.builder.models import FormStructure, FormPublished, Question

from ckeditor.widgets import CKEditor

from captcha.fields import CaptchaField

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
        if not self.target_object.rating_count or self.target_object.rating_count == 0:
            self.target_object.rating_count = 1
        self.target_object.rating_average = self.target_object.rating_sum / self.target_object.rating_count
        self.target_object.save()
        return rating_instance


class ProfileForm(forms.ModelForm):
    class Meta:
        exclude = ('membership_order',)
        model = UserProfile

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'page_for', 'title', 'content', 'provider', 'price', 'max_seats', 'location_city',
            'location_street', 'location_postal_code',
            'status',
            'date_start', 
            'date_end', 
            'bccf_topic',
            'program',
            'image',
            )
        widgets = {
            'content': CKEditor(ckeditor_config='basic'),
            'provider': forms.HiddenInput(),
            'page_for': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'date_start': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'}),
            'date_end': forms.DateTimeInput(attrs={'class':'vDatefield', 'placeholder':'YYYY-MM-DD HH:MM'}),
            'image': AdvancedFileInput(),
        }

    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if user:
            q = Q(users=user)
            if user.profile.is_level_C:
                q = q | Q(users=None)
            self.fields['program'].queryset = Program.objects.filter(q)

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('title', 'content', 'status', 'bccf_topic', 'page_for', 'image', 'user', 'by_user', 'approve')
        widgets = {
            'content': CKEditor(ckeditor_config='basic'),
            'image': AdvancedFileInput(),
            'approve': forms.HiddenInput,
            'status': forms.HiddenInput,
            'user': forms.HiddenInput,
            'by_user': forms.HiddenInput
        }

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

# GLOBAL
    
def to_mailing_list(email, add=True):
    """
    Add or remove email from MailChimp mailing list
    """
    pass

class CreateAccountForm(UserCreationForm): 

    MEMBERSHIP_TYPES = (
        ('parent', 'Parent'),
        ('professional', 'Professional'),
        ('organization', 'Organization')    
    )
    MEMBERSHIP_LEVELS = (
        ('A', 'Free'),
        ('B', 'Regular'),
        ('level_C', 'Premium')    
    )
    PAYMENT_TYPES = (
        ('Annual', 'Annual'),
        ('Quarterly', 'Quarterly'),
        ('Monthly', 'Monthly')    
    )

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    membership_type = forms.ChoiceField(required=True, choices=MEMBERSHIP_TYPES)
    gender = forms.ChoiceField(required=True, choices=UserProfile.GENDER_TYPES)
    in_mailing_list = forms.BooleanField(label='Please add me to your mailing list', required=False)
    show_in_list = forms.BooleanField(required=False)
    accept = forms.BooleanField(required=True)
    password2 = forms.CharField(label='Password (again)', required=True, widget=forms.PasswordInput)
    photo = forms.CharField(widget=AdvancedFileInput, required=False)
    payment_frequency = forms.ChoiceField(required=True, choices=PAYMENT_TYPES,
        help_text='Ignored if Level A is chosen.')
    membership_level = forms.ChoiceField(required=True, choices=MEMBERSHIP_LEVELS)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        
    def handle_upload(self):
         image_path = 'uploads/profile-photos/'+self.files['photo'].name
         destination = open(MEDIA_ROOT+'/'+image_path, 'wb+')
         for chunk in self.files['photo'].chunks():
             destination.write(chunk)
         destination.close()
         return image_path 
        
    def save(self, *args, **kwargs):
        user = super(CreateAccountForm, self).save(*args, **kwargs)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()      
        
        profile = user.profile    

        if 'photo' in self.files:
            profile.photo = self.handle_upload()

        profile.postal_code = self.cleaned_data['postal_code']
        profile.membership_type = self.cleaned_data['membership_type']
        profile.gender = self.cleaned_data['gender']
        profile.in_mailing_list = self.cleaned_data['in_mailing_list']
        profile.show_in_list = self.cleaned_data['show_in_list']
        profile.save(create_number=True)

class ProfileFieldsForm(forms.ModelForm):
        postal_code = forms.CharField(required=True)
        gender = forms.ChoiceField(required=True, choices=UserProfile.GENDER_TYPES)
        
        class Meta:
            model = UserProfile
            fields = ('postal_code', 'membership_type', 'gender', 'organization')
            widgets = {
                'organization': forms.HiddenInput,
                'membership_type': forms.HiddenInput
            }
        
        def save(self, *args, **kwargs):
            user = User.objects.get(id=self.data['organization'])
            self.instance.organization = user.profile
            self.instance.membership_type = self.data['membership_type']
            self.instance.postal_code = self.data['postal_code']
            self.instance.save(create_number=True)

class AddUserForm(Html5Mixin, forms.ModelForm):
    '''This form is used by an organization user.
    '''
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

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
        #if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
        #    settings.ACCOUNTS_APPROVAL_REQUIRED):
        #    user.is_active = False
        #    user.save()
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
            log.debug('Analyzing form item: %s=%s' % (k, v))
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
    user = forms.IntegerField(widget=forms.HiddenInput)

    def save(self):
        user = User.objects.get(pk=self.cleaned_data['user'])
        profile = user.profile
        profile.organization = None
        profile.save()
        log.debug('User %s organization is now %s' % (user, profile.organization))
        
class ReqProgram(forms.ModelForm):
    class Meta:
        model = ProgramRequest
        fields = ['title', 'comment', 'user']
        widgets = {
            'user': forms.HiddenInput()        
        }
        
# Update Profile Forms
class PhotoForm(forms.ModelForm):
    photo = forms.CharField(widget=AdvancedFileInput)
    
    class Meta:
        model = UserProfile
        fields = ('photo',)
    
    def handle_upload(self):
        image_path = 'uploads/profile-photos/'+self.files['photo'].name
        destination = open(MEDIA_ROOT+'/'+image_path, 'wb+')
        for chunk in self.files['photo'].chunks():
            destination.write(chunk)
        destination.close()
        return image_path
        
    def save(self, *args, **kwargs):
        user = self.instance
        if 'photo' in self.files and self.data['update-photo'] == 'Save':
            user.photo = self.handle_upload()
        else:
            user.photo = 'uploads/profile-photos/default_user-image-%s.gif' % user.profile.gender
        user.save()

class AccountInformationForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password (again)', required=False, widget=forms.PasswordInput)    
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'postal_code', 'email', 'username') 
        
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
        try:
            user = User.objects.get(email=email)
            if user.pk != self.instance.pk:
                raise forms.ValidationError("This email is already registered")
        except User.DoesNotExist:
            pass
            
        return email
        
    def save(self, *args, **kwargs):
        user = self.instance
        qs = User.objects.exclude(id=user.id)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)       

        user.save()
        
        profile = user.profile 
        profile.postal_code = self.cleaned_data['postal_code']
        profile.save()
        
class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('organization', 'job_title', 'website', 'phone_primary', 'street', 'street_2', 'city', 'province', 'postal_code', 'country')
    
    def __init__(self, *args, **kwargs):
        super(ContactInformationForm, self).__init__(*args, **kwargs)
        self.fields['organization'].widget.choices = self.get_organizations()
        if self.instance.is_organization or not self.instance.is_level_A:
            del self.fields['organization']
            
    def get_organizations(self):
        return User.objects.filter(profile__membership_type__exact='organization').values_list('id', 'first_name')
        
class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description', 'accreditation')
        widgets = {
            'accreditation': forms.CheckboxSelectMultiple        
        }
 
class AffiliationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('membership_level', 'membership_type')
               
class AccountPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('show_in_list', 'in_mailing_list', 'membership_level')
        
class ForumPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('show_signatures', 'signature', 'signature_html')
        
class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('facebook', 'twitter', 'linkedin', 'youtube', 'pinterest', 'othersm')
        
class RegisterUserForm(forms.Form):
    """
    Form to register organization members to professional-only events.
    """
    members = forms.MultipleChoiceField(widget=forms.SelectMultiple)
    event = forms.ChoiceField()
    
    def __init__(self, request, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        org_members = User.objects.filter(profile__organization=request.user.profile).values_list('id', 'last_name')
        events_available = Event.objects.published().filter(page_for='professional').values_list('id', 'title')
        self.fields['members'].widget.choices = org_members
        self.fields['event'].widget.choices = events_available
