import logging
from datetime import datetime
from decimal import Decimal

from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Order, ProductVariation
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import permalink, ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse

from mezzanine.conf import settings as mezzanine_settings
from mezzanine.generic.fields import RatingField, CommentsField
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable, RichText
from mezzanine.pages.fields import MenusField
from mezzanine.pages.managers import PageManager
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to, AdminThumbMixin
from mezzanine.utils.urls import path_to_slug, slugify

from bccf.fields import MyImageField
from bccf.settings import (OPTION_SUBSCRIPTION_TERM,
                           get_option_number,)
from mezzanine.utils.email import send_mail_template


log = logging.getLogger(__name__)

# Order statuses
ORDER_STATUS_COMPLETE = 2
ORDER_STATUS_CANCELLED = 3

#### Marquee Stuff ####

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
    def save(self, **kwargs):
        if self.active:
            try:
                temp = HomeMarquee.objects.get(active=True)
                if self != temp:
                    temp.active = False
                    temp.save()
            except ObjectDoesNotExist:
                self.active = True
        super(HomeMarquee, self).save(**kwargs)

class FooterMarquee(Marquee):
    active = models.BooleanField("Active", default=False,
        help_text = "Checking this will make this the default footer marquee"
    )
    def save(self, **kwargs):
        if self.active:
            try:
                temp = FooterMarquee.objects.get(active=True)
                if self != temp:
                    temp.active = False
                    temp.save()
            except ObjectDoesNotExist:
                self.active = True
        super(FooterMarquee, self).save(**kwargs)

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

#### MARQUEE STUFF END ####

#### PAGE STUFF ####

class BCCFBasePage(Orderable, Displayable):
    objects = PageManager()

    class Meta:
        abstract = True

#Subclassing Mezzanine Pages
class BCCFPage(Page, RichText):
    """
    BCCF Custom Page! This is used to streamline the URL, the child page generation,
    and everything else. This is built based on Mezzanine Page
    """
    COLORS = (
        ('dgreen-list', 'Dark Green'),
        ('green-list', 'Green'),
        ('teal-list', 'Teal'),
        ('yellow-list', 'Yellow'),
    )
    marquee = models.ForeignKey(PageMarquee, blank=True, null=True)
    carousel_color = models.CharField(max_length=11, default='dgreen-list', choices=COLORS)

    class Meta:
        verbose_name = 'BCCF Page'
        verbose_name_plural = 'BCCF Pages'

#Topic
class BCCFTopic(Displayable, RichText):
    """
    Special page for topic.
    """
    COLORS = (
        ('dgreen-list', 'Dark Green'),
        ('green-list', 'Green'),
        ('teal-list', 'Teal'),
        ('yellow-list', 'Yellow'),
    )
    marquee = models.ForeignKey(PageMarquee, blank=True, null=True)
    carousel_color = models.CharField(max_length=11, default='dgreen-list', choices=COLORS)
    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug
        return reverse('topic-page', kwargs={'topic': slug})

#BCCF Child Class Pages
class BCCFChildPage(BCCFBasePage, RichText, AdminThumbMixin):
    """
    This is the page that shows up in the fancy carousels. A copy of the Page model from Mezzanine in order to create
    its own tree-like sorting structure.
    """
    TYPES = (
        ('parent', 'Parents'),
        ('professional', 'Professionals'),
    )

    parent = models.ForeignKey('BCCFChildPage', blank=True, null=True)
    gparent = models.ForeignKey('BCCFPage', blank=True, null=True)
    bccf_topic = models.ManyToManyField('BCCFTopic', blank=True, null=True)
    featured = models.BooleanField('Featured', default=False)
    titles = models.CharField(editable=False, max_length=1000, null=True)
    content_model = models.CharField(editable=False, max_length=50, null=True, blank=True)
    login_required = models.BooleanField("Login required", default=False,
        help_text="If checked, only logged in users can view this page")
    rating = RatingField(verbose_name='Rating')
    comments = CommentsField()
    in_menus = MenusField("Show in menus", blank=True, null=True)
    page_for = models.CharField('Type', max_length=13, default='parent', blank=True, null=True, choices=TYPES)
    image = FileField("Image",
        upload_to = upload_to("bccf.ChildPage.image_file", "childpage"),
        extensions = ['.png', '.jpg', '.bmp', '.gif'],
        max_length = 255,
        null = True,
        blank = True,
        help_text = 'You can upload an image. '
            'Acceptable file types: .png, .jpg, .bmp, .gif.')

    class Meta:
        verbose_name = 'BCCF Child Page'
        verbose_name_plural = 'BCCF Child Pages'
        ordering = ("titles",)
        order_with_respect_to = "parent"

    def __unicode__(self):
        if self.parent is None and self.gparent is not None:
            return '%s: %s' % (self.gparent.title, self.title)
        elif self.gparent is None and self.parent is not None:
            return '%s: %s' % (self.parent.title, self.title)
        else:
            return self.title

    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug
        if self.gparent:
            parent = self.gparent.slug
        else:
            parent = self.parent.slug
        return reverse('bccf-child', kwargs={"parent": parent, "child": slug})

    def save(self, *args, **kwargs):
        """
        Create the titles field using the titles up the parent chain
        and set the initial value for ordering.
        """
        if self.id is None:
            self.content_model = self._meta.object_name.lower()
        titles = [self.title]
        parent = self.parent
        while parent is not None:
            titles.insert(0, parent.title)
            parent = parent.parent
        self.titles = " / ".join(titles)
        super(BCCFChildPage, self).save(*args, **kwargs)

    def description_from_content(self):
        """
        Override ``Displayable.description_from_content`` to load the
        content type subclass for when ``save`` is called directly on a
        ``Page`` instance, so that all fields defined on the subclass
        are available for generating the description.
        """
        if self.__class__ == BCCFChildPage:
            content_model = self.get_content_model()
            if content_model:
                return content_model.description_from_content()
        return super(BCCFChildPage, self).description_from_content()

    def get_ascendants(self, for_user=None):
        """
        Returns the ascendants for the page. Ascendants are cached in
        the ``_ascendants`` attribute, which is populated when the page
        is loaded via ``Page.objects.with_ascendants_for_slug``.
        """
        if not self.parent_id:
            # No parents at all, bail out.
            return []
        if not hasattr(self, "_ascendants"):
            # _ascendants has not been either page.get_ascendants or
            # Page.objects.assigned by with_ascendants_for_slug, so
            # run it to see if we can retrieve all parents in a single
            # query, which will occur if the slugs for each of the pages
            # have not been customised.
            if self.slug:
                kwargs = {"for_user": for_user}
                pages = BCCFChildPage.objects.with_ascendants_for_slug(self.slug,
                                                              **kwargs)
                self._ascendants = pages[0]._ascendants
            else:
                self._ascendants = []
        if not self._ascendants:
            # Page has a parent but with_ascendants_for_slug failed to
            # find them due to custom slugs, so retrieve the parents
            # recursively.
            child = self
            while child.parent_id is not None:
                self._ascendants.append(child.parent)
                child = child.parent
        return self._ascendants

    @classmethod
    def get_content_models(cls):
        """
        Return all Page subclasses.
        """
        is_content_model = lambda m: m is not BCCFChildPage and issubclass(m, BCCFChildPage)
        return list(filter(is_content_model, models.get_models()))

    def get_content_model(self):
        """
        Provies a generic method of retrieving the instance of the custom
        content type's model for this page.
        """
        return getattr(self, self.content_model, None)

    def get_slug(self):
        """
        Recursively build the slug from the chain of parents.
        """
        slug = slugify(self.title)
        if self.parent is not None:
            return "%s/%s" % (self.parent.slug, slug)
        return slug

    def set_slug(self, new_slug):
        """
        Changes this page's slug, and all other pages whose slugs
        start with this page's slug.
        """
        for page in BCCFChildPage.objects.filter(slug__startswith=self.slug):
            if not page.overridden():
                page.slug = new_slug + page.slug[len(self.slug):]
                page.save()
        self.slug = new_slug

    def set_parent(self, new_parent):
        """
        Change the parent of this page, changing this page's slug to match
        the new parent if necessary.
        """
        self_slug = self.slug
        old_parent_slug = self.parent.slug if self.parent else ""
        new_parent_slug = new_parent.slug if new_parent else ""

        # Make sure setting the new parent won't cause a cycle.
        parent = new_parent
        while parent is not None:
            if parent.pk == self.pk:
                raise AttributeError("You can't set a page or its child as"
                                     " a parent.")
            parent = parent.parent

        self.parent = new_parent
        self.save()

        if self_slug:
            if not old_parent_slug:
                self.set_slug("/".join((new_parent_slug, self.slug)))
            elif self.slug.startswith(old_parent_slug):
                new_slug = self.slug.replace(old_parent_slug,
                                             new_parent_slug, 1)
                self.set_slug(new_slug.strip("/"))

    def overridden(self):
        """
        Returns ``True`` if the page's slug has an explicitly defined
        urlpattern and is therefore considered to be overridden.
        """
        from mezzanine.pages.views import page
        page_url = reverse("page", kwargs={"slug": self.slug})
        resolved_view = resolve(page_url)[0]
        return resolved_view != page

    def can_add(self, request):
        """
        Dynamic ``add`` permission for content types to override.
        """
        return self.slug != "/"

    def can_change(self, request):
        """
        Dynamic ``change`` permission for content types to override.
        """
        return True

    def can_delete(self, request):
        """
        Dynamic ``delete`` permission for content types to override.
        """
        return True

    def set_helpers(self, context):
        """
        Called from the ``page_menu`` template tag and assigns a
        handful of properties based on the current page, that are used
        within the various types of menus.
        """
        current_page = context["_current_page"]
        current_page_id = getattr(current_page, "id", None)
        current_parent_id = getattr(current_page, "parent_id", None)
        # Am I a child of the current page?
        self.is_current_child = self.parent_id == current_page_id
        self.is_child = self.is_current_child  # Backward compatibility
        # Is my parent the same as the current page's?
        self.is_current_sibling = self.parent_id == current_parent_id
        # Am I the current page?
        try:
            request = context["request"]
        except KeyError:
            # No request context, most likely when tests are run.
            self.is_current = False
        else:
            self.is_current = self.slug == path_to_slug(request.path_info)

        # Is the current page me or any page up the parent chain?
        def is_c_or_a(page_id):
            parent_id = context["_parent_page_ids"].get(page_id)
            return self.id == page_id or (parent_id and is_c_or_a(parent_id))
        self.is_current_or_ascendant = lambda: bool(is_c_or_a(current_page_id))
        self.is_current_parent = self.id == current_parent_id
        # Am I a primary page?
        self.is_primary = self.parent_id is None
        # What's an ID I can use in HTML?
        self.html_id = self.slug.replace("/", "-")
        # Default branch level - gets assigned in the page_menu tag.
        self.branch_level = 0

    def in_menu_template(self, template_name):
        if self.in_menus is not None:
            for i, l, t in mezzanine_settings.PAGE_MENU_TEMPLATES:
                if not str(i) in self.in_menus and t == template_name:
                    return False
        return True

class BCCFGenericPage(BCCFChildPage):
    class Meta:
        verbose_name = 'BCCF Generic Page'
        verbose_name_plural = 'BCCF Generic Pages'

class BCCFBabyPage(BCCFChildPage):
    class Meta:
        verbose_name = 'BCCF Baby Page'
        verbose_name_plural = 'BCCF Baby Pages'

    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug.split('/')
        parent = self.parent.slug
        gparent = self.parent.gparent.slug
        return reverse('bccf-baby', kwargs={"parent": gparent, "child": parent, "baby": slug[1]})

#Article
class DocumentResourceBase(BCCFChildPage):
    #Document Fields
    attached_document = FileField('Downloadable Document',
        upload_to = upload_to("bccf.DocumentResource.attachment_file", "resource/document"),
        extensions = ['.doc','.pdf','.rtf','.txt','.odf','.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
        max_length = 255,
        null = True,
        blank = True,
        help_text = 'You can upload an office document or a PDF file. This field is not used by Video '
            'Acceptable file types: .doc, .pdf, .rtf, .txt, .odf, .docx, .xls, .xlsx, .ppt, .pptx.')
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='resources')
        super(DocumentResourceBase, self).save(**kwargs)
    class Meta:
        abstract = True

class Article(DocumentResourceBase):
    def get_resource_type(self):
        return 'Article'

class DownloadableForm(DocumentResourceBase):
    class Meta:
        verbose_name = 'Downloadable Form'
        verbose_name_plural = 'Downloadable Forms'
    def get_resource_type(self):
        return 'Downloadable Form'

class Magazine(DocumentResourceBase):
    def get_resource_type(self):
        return 'Magazine'

class TipSheet(DocumentResourceBase):
    class Meta:
        verbose_name = 'Tip Sheet'
        verbose_name_plural = 'Tip Sheets'
    def get_resource_type(self):
        return 'Tip Sheet'

class Video(BCCFChildPage):
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
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='resources')
        super(Video, self).save(**kwargs)
    def get_resource_type(self):
        return 'Video'

#Program Pages
class Program(BCCFChildPage):
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='programs')
        super(Program, self).save(**kwargs)
    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

#Blog Pages
class Blog(BCCFChildPage):
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='blog')
        super(Blog, self).save(**kwargs)
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

#TAG
class Campaign(BCCFChildPage):
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='tag')
        super(Campaign, self).save(**kwargs)

#### PAGE STUFF END ####

#### USER STUFF ####

class UserProfile(models.Model):
    MEMBERSHIP_TYPES = [
            ('parent', 'Parent'),
            ('professional', 'Professional'),
            ('organization', 'Organization'),
            ('corporate', 'Corporate'),
    ]

    user = models.OneToOneField(User, related_name='profile')
    description = models.TextField('Description', null=True, blank=True)
    photo = MyImageField(verbose_name="Photo",
        upload_to=upload_to("bccf.Profile.photo", "uploads/profile-photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"
    membership_order = models.ForeignKey('shop.Order', null=True, blank=True)
    requested_cancellation = models.NullBooleanField(null=True, blank=True, default=False)
    is_forum_moderator = models.NullBooleanField(null=True, blank=True, default=False)
    membership_type = models.CharField('Membership Type', max_length=128, null=True, blank=True, choices=MEMBERSHIP_TYPES)
    membership_level = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return 'Profile of %s' % (self.user.get_full_name() or self.user.username)

    def can_post_on_forum(self, post):
        return self.is_forum_moderator

    def set_membership_order(self, order):
        self.membership_order = order
        # Update membership type and level
        variation = self.membership_product_variation
        categ_name = variation.product.categories.all()[0].title.lower()
        self.membership_level = variation.unit_price
        self.membership_type = None
        for label, _descr in self.MEMBERSHIP_TYPES:
            if label in categ_name:
                self.membership_type = label

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
                        if is_product_variation_categ(variation, 'Membership'):
                            self.set_membership_order(order)
                            self.save()
                            return variation
            return None
        for order_item in self.membership_order.items.all():
            variation = ProductVariation.objects.get(sku=order_item.sku)
            if is_product_variation_categ(variation, 'Membership'):
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


def is_product_variation_categ(variation, categ):
    for category in variation.product.categories.all():
        if category.title.startswith(categ):
            return True

#### USER STUFF END ####

class EventBase(BCCFChildPage):
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

    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='trainings')
        self.page_for = 'parent'
        super(EventForParents, self).save(**kwargs)

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
    survey_before = models.ForeignKey('builder.FormPublished', null=True, blank=True, related_name='survey_before')
    survey_after = models.ForeignKey('builder.FormPublished', null=True, blank=True, related_name='survey_after')

    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='trainings')
        self.page_for = 'professional'
        super(EventForProfessionals, self).save(**kwargs)

        # For Surveys
        if self.survey_before:
            self.survey_before.parent = self
            self.survey_before.save()
        if self.survey_after:
            self.survey_after.parent = self
            self.survey_after.save()

    @permalink
    def signup_url(self):
        return ('professionals-event-signup', (), {'slug': self.slug})

    @permalink
    def create_url(self):
        return('professionals-event-create', (), {})

    def get_report_url(self):
        return reverse('event-survey-report', kwargs={'slug': self.slug})

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

def remaining_subscription_balance(purchase_date, expiration_date, to_date, paid):
    if not expiration_date:
        return paid
    licensed_time = expiration_date - purchase_date
    elapsed_time = to_date - purchase_date
    used_fraction = elapsed_time.total_seconds() / licensed_time.total_seconds()
    remaining = Decimal(str(float(paid) * (1 - used_fraction)))
    return remaining
