from django.db import models
from django.contrib.auth.models import User
from bccf.fields import MyImageField
from mezzanine.utils.models import upload_to
from cartridge.shop.models import Product
from django.conf import settings
from mezzanine.core.models import Slugged, Displayable, RichText
from django.db.models import permalink
from cartridge.shop.fields import MoneyField
from mezzanine.core.fields import RichTextField


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
    def membership_product(self):
        if not self.membership_order:
            return None
        for order_item in self.membership_order.items.all():
            product = Product.objects.get(sku=order_item.sku)  # @UndefinedVariable get
            for category in product.categories.all():
                if category.title.startswith('Membership'):
                    return product


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
