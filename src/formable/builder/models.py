import logging

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

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

    title = models.CharField(_("Form Title"), max_length=100)
    structure = models.TextField(_("Form Sturcture"))
    type = models.CharField(_("Form Type"), max_length=4, choices=FORM_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Form Structure")
        verbose_name_plural = _("Form Structures")
        
    def __unicode__(self):
        return self.title
        
class FormFilled(models.Model):
    """
    Model for when a form is filled out.
    """
    form_structure = models.ForeignKey('FormStructure')
    user = models.ForeignKey(User)
    filled = models.DateTimeField(_('Date Filled'), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Form Filled")
        verbose_name_plural = _("Forms Filled")
    
    def __unicode__(self):
        return self.form_structure
        
class Question(models.Model):
    """
    Model for a question in the form.
    """
    question = models.CharField(_("Question"), max_length=100)
    form_structure = models.ForeignKey('FormStructure')
    form_filled = models.ForeignKey('FormFilled')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        
    def __unicode__(self):
        return self.question
        
class FieldAnswer(models.Model):
    """
    Model for a field when a user answers the form. Multiple rows will be used to
    store each question.
    """
    answer = models.TextField(_("Answer"))
    question = models.ForeignKey("Question")
    form_filled = models.ForeignKey("FormFilled")
    answered = models.DateTimeField(_('Date Answered'), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Field Answer")
        verbose_name_plural = _("Field Answers")
    
    def __unicode__(self):
        return self.answer
