import logging
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from bccf.models import BCCFChildPage, BCCFPage

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

    title = models.CharField(_("Form Title"), default="Form Structure", max_length=100)
    structure = models.TextField(_("Form Structure"))
    type = models.CharField(_("Form Type"), max_length=4, default='JSON', choices=FORM_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Form Structure")
        verbose_name_plural = _("Form Structures")
        
    def __unicode__(self):
        return self.title
        
class FormPublished(BCCFChildPage):
    """
    Model for a published form structure.
    """
    form_structure = models.ForeignKey('FormStructure', editable=False)
    user = models.ForeignKey(User)
    
    class Meta:
        verbose_name = _("Published Form")
        verbose_name_plural = _("Published Forms")        
        
    def save(self, **kwargs):
        if self.pk is None:
            self.gparent = BCCFPage.objects.get(slug='tag')
            self.published = datetime.now()
            self.title = self.form_structure.title
        super(FormPublished, self).save(**kwargs)
    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug
        if self.parent:
            return self.parent.get_absolute_url()
        else:
            return self.get_survey_url()
    def get_survey_url(self):
        slug = self.slug        
        return reverse('formable-view', kwargs={'slug':slug})
    def get_report_url(self):
        if self.slug:
            return reverse('survey-report', kwargs={'slug': self.slug})

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
