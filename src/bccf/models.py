import logging

from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Order, ProductVariation
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import Displayable, Ownable, RichText
from mezzanine.utils.models import upload_to, AdminThumbMixin

from bccf.fields import MyImageField
from bccf.settings import (OPTION_SUBSCRIPTION_TERM, get_option_number,
    INSTALLED_APPS)


log = logging.getLogger(__name__)


class Topic(models.Model):
    name = models.CharField(max_length=255)
    star_blog_id = models.IntegerField(null=True, blank=True)
    star_survey_id = models.IntegerField(null=True, blank=True)
    star_forum_post_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class TopicLink(models.Model):
    topic = models.ForeignKey(Topic)
    model_name = models.CharField(max_length=255)
    entity_id = models.IntegerField()

    @property
    def target_model(self):
        for appname in INSTALLED_APPS:
            try:
                module = __import__('%s.models' % appname).models
                for attrname in dir(module):
                    attr = getattr(module, attrname)
                    try:
                        if self.model_name == attr._meta.db_table:
                            return attr
                        else:
                            pass
                            #log.debug('Nope, %r != %r' % (self.model_name, attr._meta.db_table))
                    except:
                        pass
                        #log.debug('Failed to get table from %s.%s' % (appname, attrname))
            except:
                pass
                #log.debug('Failed to import %s.models' % (appname, ))

    @property
    def target(self):
        model_class = self.target_model
        if not model_class:
            return None
        return model_class.objects.get(pk=self.entity_id)

    def __unicode__(self):
        return '%s - %s' % (self.topic.name, self.target)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = MyImageField(verbose_name="Photo",
        upload_to=upload_to("bccf.Profile.photo", "uploads/profile-photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"
    membership_order = models.ForeignKey('shop.Order', null=True, blank=True)
    is_forum_moderator = models.NullBooleanField(null=True, blank=True, default=False)

    def __unicode__(self):
        return 'Profile of %s' % (self.user.get_full_name() or self.user.username)

    def can_post_on_forum(self, post):
        return self.is_forum_moderator

    @property
    def membership_product_variation(self):
        if not self.membership_order:
            # Special case: if this user has purchased anything at all, there might be a recent membership purchase
            # In this case, we assign the most recent membership purchase as the membership order for this user.
            for order in Order.objects.filter(user_id=self.user_id).order_by('-time'):  # @UndefinedVariable
                for order_item in order.items.all():
                    variation = ProductVariation.objects.get(sku=order_item.sku)
                    for category in variation.product.categories.all():
                        if category.title.startswith('Membership'):
                            self.membership_order = order
                            self.save()
                            break
                    if self.membership_order:
                        break
                if self.membership_order:
                    break
        if not self.membership_order:
            return None
        for order_item in self.membership_order.items.all():
            variation = ProductVariation.objects.get(sku=order_item.sku)
            for category in variation.product.categories.all():
                if category.title.startswith('Membership'):
                    return variation

    @property
    def membership_expiration_datetime(self):
        variation = self.membership_product_variation
        if not variation:
            return None
        options = dict([(f.name, v) for f, v in zip(variation.option_fields(), variation.options())])
        d = self.membership_order.time
        subscription_term = options.get('option%s' % get_option_number(OPTION_SUBSCRIPTION_TERM))
        if subscription_term == 'Annual':
            return d + relativedelta(years=+1)
        if subscription_term == 'Quaterly':
            return d + relativedelta(months=+3)
        if subscription_term == 'Monthly':
            return d + relativedelta(months=+1)


class EventBase(Displayable):
    '''TODO: when an event is saved, make sure an associated product is created in the right category (determined by provider)
    '''
    content = RichTextField('Event Description')
    provider = models.ForeignKey(User, blank=True, null=True)

    price = MoneyField()

    location_city = models.CharField('City', max_length=255, blank=True, null=True)
    location_street = models.CharField('Street', max_length=255, blank=True, null=True)
    location_street2 = models.CharField('Street (line2)', max_length=255, blank=True, null=True)
    location_postal_code = models.CharField('Postal Code', max_length=255, blank=True, null=True)

    date_start = models.DateTimeField('Event Start', blank=True, null=True)
    date_end = models.DateTimeField('Event End', blank=True, null=True)

    class Meta:
        abstract = True


class EventForParents(EventBase):

    @permalink
    def get_absolute_url(self):
        return ('parents-event', (), {'slug': self.slug})

    @permalink
    def signup_url(self):
        return ('parents-event-signup', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Event for Parents'
        verbose_name_plural = 'Events for Parents'


class EventForProfessionals(EventBase):
    @permalink
    def get_absolute_url(self):
        return ('professionals-event', (), {'slug': self.slug})

    @permalink
    def signup_url(self):
        return ('professionals-event-signup', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Event for Professionals'
        verbose_name_plural = 'Events for Professionals'


class Settings(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_setting(cls, name, default_value=None):
        for rec in cls.objects.filter(name=name):
            return rec.value
        retval = getattr(settings, name, default_value or '-')
        cls.objects.create(name=name, value=retval)
        return retval


class DocumentResource(Displayable, Ownable, RichText, AdminThumbMixin):
    attached_document = FileField('Downloadable Document',
        upload_to=upload_to("bccf.DocumentResource.attachment_file", "resource/document"),
        extensions=['.doc','.pdf','.rtf','.txt','.odf','.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
        max_length=255,
        null=True,
        blank=True,
        help_text='You can upload an office document or a PDF file. '
            'Acceptable file types: .doc, .pdf, .rtf, .txt, .odf, .docx, .xls, .xlsx, .ppt, .pptx.')
    class Meta:
        abstract = True


class Magazine(DocumentResource):
    pass


class Article(DocumentResource):
    pass


class TipSheet(DocumentResource):
    pass


class DownloadableForm(DocumentResource):
    pass


class Video(Displayable, Ownable, RichText, AdminThumbMixin):
    video_url = models.URLField("Video", max_length=1024, blank=True, default='', null=True,
        help_text='Paste a YouTube URL here. '
            'Example: http://www.youtube.com/watch?v=6Bm7DVqJTHo')
    link_url = models.URLField("Web Link", max_length=1024, blank=True, default='', null=True,
        help_text='A link to a web resource. '
            'The address must start with http:// or https://. '
            'For example: http://plei.publiclegaled.bc.ca')
    audio_file = FileField("Video File",
        upload_to=upload_to("bccf.Video.video_file", "resource/video"),
        extensions=['.avi', '.flv', '.mkv', '.mov', '.mp4', '.ogg', '.wmv'],
        max_length=255,
        null=True,
        blank=True,
        help_text='You can upload a video file. '
            'Acceptable file types: .avi, .flv, .mkv, .mov, .mp4, .ogg, .wmv.')
