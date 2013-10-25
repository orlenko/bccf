from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Order, ProductVariation
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Displayable
from mezzanine.utils.models import upload_to

from bccf.fields import MyImageField
from bccf.settings import OPTION_SUBSCRIPTION_TERM, get_option_number


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
    def target(self):
        return globals()[self.model_name].objects.get(pk=self.entity_id)

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

    def __unicode__(self):
        return 'Profile of %s' % (self.user.get_full_name() or self.user.username)

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
