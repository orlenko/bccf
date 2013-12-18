import logging
from datetime import datetime
from decimal import Decimal

from formable.builder.models import FormPublished
from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Order, ProductVariation
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.db.models import ObjectDoesNotExist
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import Displayable, Ownable, RichText
from mezzanine.utils.models import upload_to, AdminThumbMixin
from mezzanine.pages.models import RichTextPage

from bccf.fields import MyImageField
from bccf.settings import (OPTION_SUBSCRIPTION_TERM, get_option_number,
    INSTALLED_APPS)
from mezzanine.core.models import Slugged
from mezzanine.utils.email import send_mail_template

log = logging.getLogger(__name__)

# Order statuses
ORDER_STATUS_COMPLETE = 2
ORDER_STATUS_CANCELLED = 3

class Topic(Slugged, RichText, AdminThumbMixin):
    star_blog_id = models.IntegerField(null=True, blank=True)
    star_survey_id = models.IntegerField(null=True, blank=True)
    star_forum_post_id = models.IntegerField(null=True, blank=True)
    featured_image = MyImageField(verbose_name="Featured Image",
        upload_to=upload_to("images", "uploads/images"),
        format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "featured_image"

    def __unicode__(self):
        return self.title


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
    requested_cancellation = models.NullBooleanField(null=True, blank=True, default=False)
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
            orders = Order.objects.filter(user_id=self.user_id)
            orders = orders.exclude(status=ORDER_STATUS_CANCELLED).order_by('-time')
            for order in orders:
                for order_item in order.items.all():
                    for variation in ProductVariation.objects.filter(sku=order_item.sku):
                        for category in variation.product.categories.all():
                            if category.title.startswith('Membership'):
                                self.membership_order = order
                                self.save()
                                return variation
            return None
        for order_item in self.membership_order.items.all():
            variation = ProductVariation.objects.get(sku=order_item.sku)
            for category in variation.product.categories.all():
                if category.title.startswith('Membership'):
                    return variation

    def cancel_membership(self):
        from bccf.util.memberutil import refund

        if not self.membership_order:
            return
        membership_order = self.membership_order
        membership_order.status = ORDER_STATUS_CANCELLED
        membership_order.save()
        self.membership_order = None
        self.save()
        while self.membership_product_variation:
            old_order = self.membership_order
            old_order.status = ORDER_STATUS_CANCELLED
            old_order.save()
            self.membership_order = None
            self.save()
        refund(self.user, membership_order) # Probably unnecessary - refunds will be handled offline

    def request_membership_cancellation(self):
        self.requested_cancellation = True
        self.save()
        user = self.user
        membership_order = self.membership_order
        membership_product_variation = self.membership_product_variation
        send_mail_template('Membership cancellation requested: %s' % user.email,
                           'bccf/email/membership_cancellation_request_admin',
                           Settings.get_setting('SERVER_EMAIL'),
                           Settings.get_setting('ADMIN_EMAIL'),
                           context=locals(),
                           attachments=None,
                           fail_silently=settings.DEBUG,
                           addr_bcc=None)
        send_mail_template('Your BCCF membership cancellation request',
                           'bccf/email/membership_cancellation_request',
                           Settings.get_setting('SERVER_EMAIL'),
                           user.email,
                           context=locals(),
                           attachments=None,
                           fail_silently=settings.DEBUG,
                           addr_bcc=None)

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

    @property
    def remaining_balance(self):
        membership = self.membership_product_variation
        expiration_date = self.membership_expiration_datetime
        purchase_date = self.membership_order.time
        price = membership.unit_price
        now = datetime.now()
        return remaining_subscription_balance(purchase_date, expiration_date, now, price)


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

    @permalink
    def create_url(self):
        return('parents-event-create', (), {})

    class Meta:
        verbose_name = 'Event for Parents'
        verbose_name_plural = 'Events for Parents'


class EventForProfessionals(EventBase):
    survey_before = models.ForeignKey(FormPublished, null=True, blank=True, related_name='survey_before')
    survey_after = models.ForeignKey(FormPublished, null=True, blank=True, related_name='survey_after')

    @permalink
    def get_absolute_url(self):
        return ('professionals-event', (), {'slug': self.slug})

    @permalink
    def signup_url(self):
        return ('professionals-event-signup', (), {'slug': self.slug})

    @permalink
    def create_url(self):
        return('professionals-event-create', (), {})

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
    video_file = FileField("Video File",
        upload_to=upload_to("bccf.Video.video_file", "resource/video"),
        extensions=['.avi', '.flv', '.mkv', '.mov', '.mp4', '.ogg', '.wmv'],
        max_length=255,
        null=True,
        blank=True,
        help_text='You can upload a video file. '
            'Acceptable file types: .avi, .flv, .mkv, .mov, .mp4, .ogg, .wmv.')


def remaining_subscription_balance(purchase_date, expiration_date, to_date, paid):
    if not expiration_date:
        return paid
    licensed_time = expiration_date - purchase_date
    elapsed_time = to_date - purchase_date
    used_fraction = elapsed_time.total_seconds() / licensed_time.total_seconds()
    remaining = Decimal(str(float(paid) * (1 - used_fraction)))
    return remaining


class Marquee(models.Model):
    """
    Parent model for marquees (big marquee, footer)
    """
    title = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title

class HomeMarquee(Marquee):
    active = models.BooleanField("Active", default=False,
        help_text = "Checking this box makes this the default marquee in the home page"
    )
    def save(self):
        if self.active:
            try:
                temp = HomeMarquee.objects.get(active=True)
                if self != temp:
                    temp.active = False
                    temp.save()
            except ObjectDoesNotExist:
                self.active = True
        super(HomeMarquee, self).save()

class FooterMarquee(Marquee):
    active = models.BooleanField("Active", default=False,
        help_text = "Checking this will make this the default footer marquee"
    )

    def save(self):
        if self.active:
            try:
                temp = FooterMarquee.objects.get(active=True)
                if self != temp:
                    temp.active = False
                    temp.save()
            except ObjectDoesNotExist:
                self.active = True
        super(FooterMarquee, self).save()

class PageMarquee(Marquee):
    pass

class MarqueeSlide(models.Model):
    """
    Parent model for slides in the marquee
    """
    caption = models.CharField("Caption", max_length=100, blank=True, default='', null=True)
    title = models.CharField("Title", max_length=50, blank=True, default='', null=True)
    image = FileField("Image",
        upload_to = upload_to("bccf.MarqueeSlide.image_file", "marquee"),
        extensions = ['.png', '.jpg', '.bmp', '.gif'],
        max_length = 255,
        null = True,
        blank = True,
        help_text = 'You can upload an image. '
            'Acceptable file types: .png, .jpg, .bmp, .gif.')
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.title

class HomeMarqueeSlide(MarqueeSlide):
    marquee = models.ManyToManyField(HomeMarquee)
    url = models.URLField("Link", blank=True, default='', null=True)
    linkLabel = models.CharField("Link Label", max_length=10, blank=True, default='', null=True)

class FooterMarqueeSlide(MarqueeSlide):
    marquee = models.ManyToManyField(FooterMarquee)

class PageMarqueeSlide(MarqueeSlide):
    marquee = models.ManyToManyField(PageMarquee)
    url = models.URLField("Link", blank=True, default='', null=True)
    linkLabel = models.CharField("Link Label", max_length=10, blank=True, default='', null=True)

#Pages
class Page(RichTextPage):
    COLORS = (
        ('dgreen-list', 'Dark Green'),
        ('green-list', 'Green'),
        ('teal-list', 'Teal'),
        ('yellow-list', 'Yellow'),
    )
    marquee = models.ForeignKey(PageMarquee, blank=True, null=True)
    carouselColor = models.CharField(max_length=11, default='dgreen-list', choices=COLORS)

#Child Page
class ChildPage(RichTextPage):
    image = FileField("Image",
        upload_to = upload_to("bccf.ChildPage.image_file", "childpage"),
        extensions = ['.png', '.jpg', '.bmp', '.gif'],
        max_length = 255,
        null = True,
        blank = True,
        help_text = 'You can upload an image. '
            'Acceptable file types: .png, .jpg, .bmp, .gif.')
