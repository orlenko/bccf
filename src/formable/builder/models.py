import logging
import json
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from bccf.models import TagBase, BCCFPage
from bccf.managers import TagManager

log = logging.getLogger(__name__)

class FormStructure(models.Model):
    """
    Model for the form structure. The form structure can be stored as JSON, HTML,
    YAML, or XML.
    """
    FORM_TYPE = (
        ('JSON', 'JSON'),
        #('2', 'HTML'), # To be Implemented
        #('3', 'YAML'), # To be Implemented
        #('4', 'XML'), # To be Implemented
    )

    user = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(_("Form Title"), default="Form Structure", max_length=100)
    structure = models.TextField(_("Form Structure"))
    type = models.CharField(_("Form Type"), max_length=4, default='JSON', choices=FORM_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Form Structure")
        verbose_name_plural = _("Form Structures")
    
    @permalink
    def get_edit_url(self):
        return ('formable-edit-clone-form', (), {'type':'edit', 'id':self.pk})
    @models.permalink
    def get_clone_url(self):
        return ('formable-edit-clone-form', (), {'type':'clone', 'id':self.pk})
    @models.permalink
    def get_publish_url(self):
        return ('formable-publish-form', (), {'id':self.pk})
    
    def __unicode__(self):
        return self.title
        
class FormPublished(TagBase):
    """
    Model for a published form structure.
    """
    form_structure = models.ForeignKey('FormStructure')
    closed = models.BooleanField('Closed', default=False);
    user = models.ForeignKey(User)
    
    objects = TagManager()
    
    class Meta:
        verbose_name = _("Published Form")
        verbose_name_plural = _("Published Forms")        
        
    def __init__(self, *args, **kwargs):
        super(FormPublished, self).__init__(*args, **kwargs)        
        
    def save(self, **kwargs):
        if not self.image:
            self.image = 'uploads/childpage/placeholder-survey.png'
        if self.pk is None: 
            super(FormPublished, self).save(**kwargs)            

            struct = json.loads(self.form_structure.structure)
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
                            form_published=self, required=required,
                            num_answers=num_answers)
                        question.save()
        else:
            super(FormPublished, self).save(**kwargs)
        
    @permalink
    def get_absolute_url(self):
        return ('formable-view', (), {'slug': self.slug})
    @permalink
    def get_survey_url(self):       
        return ('formable-view', (), {'slug': self.slug})
    @permalink
    def get_report_url(self):
        return ('survey-report', (), {'slug': self.slug})

class FormFilled(models.Model):
    """
    Model for when a form is filled out.
    """
    title = models.CharField(_('Title'), max_length=100)
    form_published = models.ForeignKey('FormPublished')
    user = models.ForeignKey(User)
    filled = models.DateTimeField(_('Date Filled'), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Filled Form")
        verbose_name_plural = _("Filled Forms")
    
    def __unicode__(self):
        return self.title
        
    def save(self):
        if self.pk is None:
            self.filled = datetime.now()
            self.title = 'Filled: %s - %s %s' % (self.form_published.title,
                self.user.get_full_name() or self.user.username, 
                self.form_published.__str__())
        super(FormFilled, self).save()
        
class Question(models.Model):
    """
    Model for a question in the form.
    """
    question = models.CharField(_("Question"), max_length=100)
    form_published = models.ForeignKey('FormPublished')
    required = models.BooleanField(_("Required"))
    num_answers = models.IntegerField(_("Number of possible Answers"), default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        
    def __unicode__(self):
        return self.question
        
class FieldAnswer(models.Model):
    """
    Model for a field when a user answers the form. Multiple rows will be used to
    store each answer (ie. 5 check boxes - up to 5 rows will be stored).
    """
    answer = models.TextField(_("Answer"))
    question = models.ForeignKey("Question")
    form_filled = models.ForeignKey("FormFilled")
    answered = models.DateTimeField(_('Date Answered'), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
    
    def __unicode__(self):
        return self.answer
