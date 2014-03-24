import logging
log = logging.getLogger(__name__)

from datetime import datetime
from decimal import Decimal

from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Order, ProductVariation, Product
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import permalink, ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse

from embed_video.fields import EmbedVideoField

from mezzanine.conf import settings as mezzanine_settings
from mezzanine.generic.fields import RatingField, CommentsField
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import Displayable, Orderable, RichText
from mezzanine.pages.fields import MenusField
from mezzanine.pages.managers import PageManager
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to, AdminThumbMixin
from mezzanine.utils.urls import path_to_slug, slugify

from bccf import managers
from bccf.fields import MyImageField
from bccf.settings import (OPTION_SUBSCRIPTION_TERM,
                           get_option_number,)

from mezzanine.utils.email import send_mail_template

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
        verbose_name = 'Parent Page'
        verbose_name_plural = 'Parent Pages'
    def get_slug(self):
        slug = slugify(self.title)
        if not self.slug:
            slug = 'bccf/%s' % slug
        return slug

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
    gparent = models.ForeignKey('BCCFPage', verbose_name="Parent Page", blank=True, null=True)
    bccf_topic = models.ManyToManyField('BCCFTopic', blank=True, null=True)
    featured = models.BooleanField('Featured', default=False)
    titles = models.CharField(editable=False, max_length=1000, null=True)
    content_model = models.CharField(editable=False, max_length=50, null=True, blank=True)
    rating = RatingField(verbose_name='Rating')
    comments = CommentsField()
    page_for = models.CharField('Type', max_length=13, default='parent', blank=True, null=True, choices=TYPES)
    image = FileField("Image",
        upload_to = upload_to("bccf.ChildPage.image_file", "childpage"),
        extensions = ['.png', '.jpg', '.bmp', '.gif'],
        max_length = 255,
        null = True,
        blank = True,
        help_text = 'You can upload an image. '
            'Acceptable file types: .png, .jpg, .bmp, .gif.')

    objects = managers.ChildPageManager()

    class Meta:
        verbose_name = 'BCCF Child Page'
        verbose_name_plural = 'BCCF Child Pages'
        ordering = ("-created",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug
        parent = 'trainings'
        if self.gparent:
            if 'bccf/' in self.gparent.slug:
                rest, parent = self.gparent.slug.split('bccf/', 1)
            else:
                parent = self.gparent.slug
        elif self.parent:
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
        log.debug('Getting %s from %s' % (self.content_model, self))
        try:
            return getattr(self, self.content_model, None)
        except:
            log.debug('Failed to get it!', exc_info=1)
            return None

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
    show_resources = models.BooleanField('Show Resources', default=True)
    show_comments = models.BooleanField('Show Comments', default=True)
    show_rating = models.BooleanField('Show Rating', default=True)
    class Meta:
        verbose_name = 'Sub Page'
        verbose_name_plural = 'Sub Pages'


class BCCFBabyPage(BCCFChildPage):
    order = models.IntegerField('Order', blank=True, null=True)

    class Meta:
        verbose_name = 'Third Level Page'
        verbose_name_plural = 'Third Level Pages'
        ordering = ('order',)

    def get_absolute_url(self):
        """
        URL for a page
        """
        slug = self.slug.split('/')
        return "%s%s" % (self.parent.get_absolute_url(), slug[1])

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
    product = models.ForeignKey(Product, verbose_name='Associated Product', blank=True, null=True)
    
    def save(self, **kwargs):
        if not self.image:
            self.image = 'childpage/placeholder-resource.gif'
        self.gparent = BCCFPage.objects.get(slug='bccf/resources')
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

class Podcast(BCCFChildPage):
    attached_audio = FileField('Audio File',
       upload_to = upload_to("bccf.Podcast.attachment_audio", "resource/audio"),
        extensions = ['.mp3'],
        max_length = 1024,
        null = True,
        blank = True,
        help_text = 'You can upload an MP3. Acceptable file types: mp3')
    product = models.ForeignKey(Product, verbose_name='Associated Product', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Podcast'
        verbose_name_plural = 'Podcasts'       
    
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='bccf/resources')
        if not self.image:
            self.image = 'childpage/placeholder-podcast.gif'
        super(Podcast, self).save(**kwargs)
    def get_resource_type(self):
        return 'Podcast'

class Video(BCCFChildPage):
    video_url = EmbedVideoField("Video", max_length=1024, blank=True, default='', null=True,
    help_text='Paste a YouTube URL here. '
        'Example: http://www.youtube.com/watch?v=6Bm7DVqJTHo')
    product = models.ForeignKey(Product, verbose_name='Associated Product', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'    

    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='bccf/resources')
        if not self.image:
            self.image = 'childpage/placeholder-video.gif'
        super(Video, self).save(**kwargs)
    def get_resource_type(self):
        return 'Video'

#Program Pages
class Program(BCCFChildPage):
    users = models.ManyToManyField(User, verbose_name='Requester', blank=True, null=True)
    user_added = models.BooleanField('Added By User', default=False, blank=True) 
    
    objects = managers.ChildPageManager()    
    
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='bccf/programs')
        super(Program, self).save(**kwargs)
    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

#Blog Pages
class Blog(BCCFChildPage):
    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='bccf/blog')
        super(Blog, self).save(**kwargs)
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

#TAG
class TagBase(BCCFChildPage):
    objects = managers.TagManager()   

    class Meta:
        abstract = True

    def save(self, **kwargs):
        self.gparent = BCCFPage.objects.get(slug='bccf/tag')
        super(TagBase, self).save(**kwargs)

class Campaign(TagBase):
    user = models.ForeignKey(User, verbose_name='Created By', null=True, blank=True, related_name='campaigns')
    approve = models.BooleanField('Approve Campaign', default=True)
    approved_on = models.DateTimeField('Approved On', blank=True, null=True)
    by_user = models.BooleanField('Created By User', default=False)
    
    @permalink
    def edit_url(self):
        return('campaigns-edit', (), {'slug': self.slug})
        
    def save(self, *args, **kwargs):
        super(Campaign, self).save(*args, **kwargs)
        if not self.image:
            self.image = 'childpage/placeholder-campaign.gif'
        if self.approve:
            self.accept_request()
        
    def accept_request(self):
        if self.by_user and not self.approved_on:
            self.approve = True
            self.status = 2
            self.approved_on = datetime.now()
            self.save()

#### PAGE STUFF END ####

#### USER STUFF ####
from pybb.models import PybbProfile

class UserProfile(PybbProfile):
    """
    User Profile
    """
    MEMBERSHIP_TYPES = [
            ('parent', 'Parent'),
            ('professional', 'Professional'),
            ('organization', 'Organization'),
            ('corporate', 'Corporate'),
    ]
    GENDER_TYPES = [
            ('male', 'Male'),
            ('female', 'Female')    
    ]
    MEMBERSHIP_LEVELS = [
            ('A', 'Level A'),
            ('B', 'Level B'),
            ('C', 'Level C')    
    ]

    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField('Gender', max_length=6, default='male', blank=True, null=True, choices=GENDER_TYPES)
    description = models.TextField('Description', null=True, blank=True)
    photo = MyImageField(verbose_name="Photo",
        upload_to=upload_to("bccf.Profile.photo", "uploads/profile-photos"),
        format="Image", max_length=255, null=True, blank=True,
        help_text='User photo')
    admin_thumb_field = "photo"
    
    # Membership Fields
    membership_type = models.CharField('Membership Type', max_length=128, null=True, blank=True, choices=MEMBERSHIP_TYPES)
    membership_order = models.ForeignKey('shop.Order', null=True, blank=True, related_name='order')
    voting_order = models.ForeignKey('shop.Order', null=True, blank=True, related_name='voting')
    membership_level = models.CharField('Membership Level', max_length=1, default='A', choices=MEMBERSHIP_LEVELS)
    requested_cancellation = models.NullBooleanField(null=True, blank=True, default=False)
    
    organization = models.ForeignKey('UserProfile', null=True, blank=True, related_name='members')

    accreditation = models.ManyToManyField(Program, verbose_name='Certifications', blank=True, null=True)
    show_in_list = models.BooleanField('Show in member directory', default=False)
    in_mailing_list = models.BooleanField('In mailing list', default=False)

    is_forum_moderator = models.NullBooleanField(null=True, blank=True, default=False)

    objects = managers.UserProfileManager()

    # Member Fields
    job_title = models.CharField('Job Title', max_length=255, null=True, blank=True)
    website = models.URLField('Website', null=True, blank=True)
    phone_primary = models.CharField('Phone (Primary)', max_length=15, null=True, blank=True)
    phone_work = models.CharField('Phone (Work)', max_length=15, null=True, blank=True)
    phone_mobile = models.CharField('Phone (Mobile)', max_length=15, null=True, blank=True)
    fax = models.CharField('Fax', null=True, max_length=15, blank=True)
    street = models.CharField('Street', max_length=255, null=True, blank=True)
    street_2 = models.CharField('Street 2', max_length=255, null=True, blank=True)
    street_3 = models.CharField('Street 3', max_length=255, null=True, blank=True)
    city = models.CharField('City', max_length=255, null=True, blank=True)
    postal_code = models.CharField('Postal Code', max_length=10,)
    region = models.CharField('Region', max_length=255, null=True, blank=True)
    province = models.CharField('Province/State', max_length=255, null=True, blank=True)
    country = models.CharField('Country', max_length=255, null=True, blank=True)

    # Social
    facebook = models.CharField('Facebook', max_length=255, null=True, blank=True)
    twitter = models.CharField('Twitter', max_length=255, null=True, blank=True)
    linkedin = models.CharField('LinkedIn', max_length=255, null=True, blank=True)
    youtube = models.CharField('Youtube', max_length=255, null=True, blank=True)
    pinterest = models.CharField('Pinterest', max_length=255, null=True, blank=True)
    
    #Banking
    account_number = models.CharField('Account Number', max_length=12, null=True, blank=True)  

    def __unicode__(self):
        return 'Profile of %s' % (self.user.get_full_name() or self.user.username)

    def save(self, create_number=False, *args, **kwargs):
        if create_number:
            self.account_number = self.create_account_number()
            if not self.photo:
                self.photo = 'uploads/profile-photos/default_user-image-%s.gif' % (self.gender)
        super(UserProfile, self).save(**kwargs)

    def get_full_address(self):
        address = ''
        for part in [self.street, self.city, self.province, self.postal_code]:
            if part:
                address += part+' '
        return address

    def can_post_on_forum(self, post):
        return self.is_forum_moderator

    def set_membership_order(self, order):
        self.membership_order = order
        # Update membership type and level
        variation = self.membership_product_variation
        #categ_name = variation.product.categories.all()[0].title.lower()
        sku_parts = variation.sku.split('-')
        self.membership_level = sku_parts[1] # only get the middle one (B or C)
        #self.membership_type = None
        #for label, _descr in self.MEMBERSHIP_TYPES:
        #    if label in categ_name:
        #        self.membership_type = label

    @property
    def membership_product_variation(self):
        #ensure_membership_products()
        # Special case for admin:
        #if self.user.is_superuser:
            # Make sure current order contains an Admin-level license
            # self.ensure_membership('admin')
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

    ### Helpers to quickly determine type of membership

    @property
    def short_membership_type(self):
        membership = 'membership'
        markers = ('professional', 'parent', 'organization', 'corporate')
        membership_product_variation = self.membership_product_variation
        if membership_product_variation:
            for category in membership_product_variation.product.categories.all():
                if membership in category.slug:
                    for marker in markers:
                        if marker in category.slug:
                            return marker

    @property
    def is_level_A(self):
        return 'A' in self.membership_level

    @property
    def is_level_B(self):
        return 'B' in self.membership_level
        
    @property
    def is_level_C(self):
        return 'C' in self.membership_level

    @property
    def is_parent(self):
        return 'parent' in self.membership_type

    @property
    def is_professional(self):
        return 'professional' in self.membership_type

    @property
    def is_organization(self):
        return 'organization' in self.membership_type

    @property
    def is_corporate(self):
        return 'corporate' in self.membership_type

    @property
    def provided_event_type(self):
        memb = self.short_membership_type
        if self.user.is_superuser:
            return 'all'
        if memb == 'professional':
            return 'parent'
            
    def create_account_number(self):
        from random import randrange
        first = self.user.first_name[:3].upper()
        second = self.user.last_name[:3].upper()
        third = ''
        
        for x in range(0, 6):
            num = randrange(0, 9)
            third  += `num`
            
        return first+second+third

def is_product_variation_categ(variation, categ):
    for category in variation.product.categories.all():
        if category.title.startswith(categ):
            return True

#### USER STUFF END ####

#### PROGRAM REQUEST #####
class ProgramRequest(models.Model):
    user = models.ForeignKey(User, related_name='program_requests')
    title = models.CharField('Program Name', max_length=255)
    comment = RichTextField('Comment', blank=True, null=True, help_text='Provide a reason')
    accept = models.BooleanField('Accept', default=False)
    created = models.DateTimeField('Requested On', auto_now_add=True, blank=True, null=True)
    accepted_on = models.DateTimeField('Accepted On', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Program Request'
        verbose_name_plural = 'Program Requests'
        ordering = ('-created',)
    
    def accept_request(self):
        if self.accept:
            return
        try:
            program = Program.objects.get(title__iexact=self.title)
        except ObjectDoesNotExist:
            program = Program(title=self.title, content=self.comment, status=1, user_added=True)
        program.save()
        program.users.add(self.user)
        
        self.accepted_on = datetime.now()
        self.accept = True
        self.save()

#### PROGRAM REQUEST END ####

class Event(BCCFChildPage):
    provider = models.ForeignKey(User, blank=True, null=True, related_name='events')

    price = MoneyField()

    location_city = models.CharField('City', max_length=255, blank=True, null=True)
    location_street = models.CharField('Street', max_length=255, blank=True, null=True)
    location_street2 = models.CharField('Street (line2)', max_length=255, blank=True, null=True)
    location_postal_code = models.CharField('Postal Code', max_length=255, blank=True, null=True)

    date_start = models.DateTimeField('Event Start', blank=True, null=True)
    date_end = models.DateTimeField('Event End', blank=True, null=True)

    survey_before = models.ForeignKey('builder.FormPublished', null=True, blank=True, related_name='survey_before')
    survey_after = models.ForeignKey('builder.FormPublished', null=True, blank=True, related_name='survey_after')
    
    program = models.ForeignKey(Program, null=True, blank=True, related_name='program')
    max_seats = models.PositiveIntegerField('Max number of seats', null=True, blank=True, default=1)
    full = models.BooleanField('Event is full', blank=True, default=False)

    event_product = models.ForeignKey('shop.Product', null=True, blank=True, related_name='event-product')

    objects = managers.EventManager()

    def save(self, **kwargs):
        if not self.pk:
            gp = BCCFPage.objects.get(slug='bccf/trainings')
            self.gparent = gp
            super(Event, self).save(**kwargs)
            if self.price: # If it's not free create a product
                product = Product.objects.create(title=self.title, content=self.content)
                variation = ProductVariation.objects.create(product=product, sku='EVENT-%s' % self.pk,
                    num_in_stock=self.max_seats, default=True, unit_price=self.price)
                self.event_product = product
        super(Event, self).save(**kwargs)

    def is_full(self):
        return self.full

    @permalink
    def signup_url(self):
        return ('events-signup', (), {'slug': self.slug})

    @permalink
    def edit_url(self):
        return('events-edit', (), {'slug': self.slug})

    @permalink
    def report_url(self):
        return('event-survey-report', (), {'slug':self.slug})
        
    @permalink
    def attendee_url(self):
        return ('events-attendees', (), {'id':self.id})


EventForParents = Event
EventForProfessionals = Event

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='event_registration')
    user = models.ForeignKey(User)
    registration_date = models.DateTimeField(auto_now_add=True, blank=True)
    passed = models.BooleanField('Passed', default=False, blank=True)
    event_order = models.ForeignKey('shop.Order', null=True, blank=True, related_name='event-order')
    paid = models.BooleanField('Paid', default=False)
    
    class Meta:
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"
    
    def save(self, **kwargs):
        user = UserProfile.objects.get(user=self.user)
        if self.pk and user.membership_type == 'professional' and self.event.program:
            if self.passed:
                user.accreditation.add(self.event.program)
            else:
                user.accreditation.remove(self.event.program)
        super(EventRegistration, self).save(**kwargs)
        

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


#def ensure_membership_products():
#    '''Create default set of products, if necessary'''
#    REQUIRED_PRODUCTS = {
#        'Organization Membership': [{
#            'Subscription Term': 'Annual',
#            'Create Events for Parents': 'Accredited Programs Only',
#            'Directory Listing': 'Business Card',
#            'Store Discount': 'No',
#            'price': 100
#        }, {
#            'Subscription Term': 'FREE - Unlimited',
#            'Create Events for Parents': 'No',
#            'Directory Listing': 'Basic',
#            'Store Discount': 'No',
#            'price': 0
#        }, {
#            'Subscription Term': 'Annual',
#            'Create Events for Parents': 'Accredited and Other Programs',
#            'Directory Listing': 'Business Card',
#            'Store Discount': 'No',
#            'price': 200
#       }],
#        'Professional Membership': [],
#       'Parent Membership': [],
#        'Admin Membership': [],
#    }