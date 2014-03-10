
######################
# CARTRIDGE SETTINGS #
######################

# The following settings are already defined in cartridge.shop.defaults
# with default values, but are common enough to be put here, commented
# out, for convenient overriding.

# Sequence of available credit card types for payment.
# SHOP_CARD_TYPES = ("Mastercard", "Visa", "Diners", "Amex")

# Setting to turn on featured images for shop categories. Defaults to False.
# SHOP_CATEGORY_USE_FEATURED_IMAGE = True

# Set an alternative OrderForm class for the checkout process.
# SHOP_CHECKOUT_FORM_CLASS = 'cartridge.shop.forms.OrderForm'

# If True, the checkout process is split into separate
# billing/shipping and payment steps.
SHOP_CHECKOUT_STEPS_SPLIT = False

# If True, the checkout process has a final confirmation step before
# completion.
SHOP_CHECKOUT_STEPS_CONFIRMATION = False
SHOP_DISCOUNT_FIELD_IN_CHECKOUT = True

# Controls the formatting of monetary values accord to the locale
# module in the python standard library. If an empty string is
# used, will fall back to the system's locale.
# SHOP_CURRENCY_LOCALE = ""

# Dotted package path and class name of the function that
# is called on submit of the billing/shipping checkout step. This
# is where shipping calculation can be performed and set using the
# function ``cartridge.shop.utils.set_shipping``.
# SHOP_HANDLER_BILLING_SHIPPING = \
#                           "cartridge.shop.checkout.default_billship_handler"

# Dotted package path and class name of the function that
# is called once an order is successful and all of the order
# object's data has been created. This is where any custom order
# processing should be implemented.
SHOP_HANDLER_ORDER = "bccf.util.memberutil.order_handler"

# Dotted package path and class name of the function that
# is called on submit of the payment checkout step. This is where
# integration with a payment gateway should be implemented.
# SHOP_HANDLER_PAYMENT = "cartridge.shop.checkout.default_payment_handler"

# Sequence of value/name pairs for order statuses.
SHOP_ORDER_STATUS_CHOICES = (
    (1, "Unprocessed"),
    (2, "Processed"),
    (3, "Cancelled"),
)

# Sequence of value/name pairs for types of product options,
# eg Size, Colour.

# Option names
OPTION_SUBSCRIPTION_TERM = 'Subscription Term'
OPTION_BCCF_VOTING = 'BCCF Voting'
OPTION_CREATE_EVENTS_FOR_PARENTS = 'Create Events for Parents'
OPTION_DIRECTORY_LISTING = 'Directory Listing'
OPTION_STORE_DISCOUNT = 'Store Discount'


SHOP_OPTION_TYPE_CHOICES = [(i+1, label) for i, label in enumerate([

    # Period of subscription - annual, quarterly, monthly
    OPTION_SUBSCRIPTION_TERM,

    # Parent membership perks
    OPTION_BCCF_VOTING,

    # Professional membership perks
    OPTION_CREATE_EVENTS_FOR_PARENTS, # Level 2: accredited programs only; Level 3: +other program types
    OPTION_DIRECTORY_LISTING, # Level 1: basic listing; Level 2: Business Card style; Level 3: High Profile Listing
    OPTION_STORE_DISCOUNT, # Level 3: 15% discount

])]

def get_option_number(option_name):
    for num, name in SHOP_OPTION_TYPE_CHOICES:
        if name == option_name:
            return num


def get_option_name(option_number):
    for num, name in SHOP_OPTION_TYPE_CHOICES:
        if num == option_number:
            return name


######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
ADMIN_MENU_ORDER = (
    ("Content", ("pages.Page", "bccf.BCCFGenericPage", "bccf.BCCFTopic",
       "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
    ("Site", ("sites.Site", "redirects.Redirect", "bccf.Settings", "conf.Setting")),
    ("Users", ("auth.User", "auth.Group",)),
    ("Blogs", ("bccf.Blog",)),
    ("Campaigns", ("bccf.Campaign",)),
    ("Events", ("bccf.Event",)),
    ("Marquees", ("bccf.HomeMarquee", "bccf.HomeMarqueeSlide", "bccf.PageMarquee", "bccf.PageMarqueeSlide", "bccf.FooterMarquee", "bccf.FooterMarqueeSlide")),
    ("News", ("news.NewsPost",)),
    ("Programs", ("bccf.Program", "bccf.ProgramRequest")),
    ("Resources", ("bccf.Article", "bccf.DownloadableForm", "bccf.Magazine", "bccf.TipSheet", "bccf.Video")),
    ("Forum", ("pybb.Forum", "pybb.Topic", "pybb.Post", "pybb.Profile")),
)

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, "Top navigation bar", "pages/menus/dropdown.html"),
#     (2, "Left-hand tree", "pages/menus/tree.html"),
#     (3, "Footer", "pages/menus/footer.html"),
# )

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
# BLOG_USE_FEATURED_IMAGE = True

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting.
USE_SOUTH = True


########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make these unique, and don't share it with anybody.
SECRET_KEY = "ac80eaea-1f51-42ed-ab04-821a5126563f5828551c-1116-44df-9dd4-72809374476d4b168d32-46df-4462-942a-959cdf9c8bcc"
NEVERCACHE_KEY = "2985023f-d904-479b-8c2d-fa0f2034b44f4fb12480-8a99-49e0-88bc-bc763f2245cfa2234156-1a5b-43f5-999c-71bc47751b1a"

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1", "67.231.18.161")

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    'ckeditor',
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.forms",
    "mezzanine.pages",
    #"mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    #"mezzanine.blog",
    #"mezzanine.mobile",
    'news',
    'pybb',
    'bccf',
    "cartridge.shop",
    'formable.builder',
    # install via pip or easy_install django-form-utils
    'form_utils', # required by builder to call template tags
    'embed_video',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    'pybb.context_processors.processor',
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
    'pybb.middleware.PybbMiddleware',
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

def forum_instant_post(user, post):
    if user.profile:
        return user.profile.can_post_on_forum(post)
    return False

PYBB_PREMODERATION = forum_instant_post
PYBB_PROFILE_RELATED_NAME = 'profile'

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,'ckeditor',
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
###################
# DEPLOY SETTINGS #
###################

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "SSH_USER": "", # SSH username
#     "SSH_PASS":  "", # SSH password (consider key-based authentication)
#     "SSH_KEY_PATH":  "", # Local path to SSH key file, for key-based auth
#     "HOSTS": [], # List of hosts to deploy to
#     "VIRTUALENV_HOME":  "", # Absolute remote path for virtualenvs
#     "PROJECT_NAME": "", # Unique identifier for project
#     "REQUIREMENTS_PATH": "", # Path to pip requirements, relative to project
#     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#     "LIVE_HOSTNAME": "www.example.com", # Host for public site.
#     "REPO_URL": "", # Git or Mercurial remote repo URL for the project
#     "DB_PASS": "", # Live database password
#     "ADMIN_PASS": "", # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }


AUTH_PROFILE_MODULE = 'bccf.UserProfile'
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = [
    'membership_order',
    'is_forum_moderator',
    'membership_type',
    'membership_level',
    'requested_cancellation',
    'signature',
    'signature_html',
    'time_zone',
    'language',
    'show_signatures',
    'post_count',
    'avatar',
    'autosubscribe',
    'job_title',
    'website',
    'facebook',
    'twitter',
    'linkedin',
]
ACCOUNTS_PROFILE_VIEWS_ENABLED = True
ACCOUNTS_VERIFICATION_REQUIRED = True

GRAPPELLI_ADMIN_TITLE = 'BCCF'
GRAPPELLI_ADMIN_HEADLINE = 'BCCF'

ALLOWED_HOSTS = ['*']


#######################
# MEMBERSHIP SETTINGS #
#######################

PARENT_MEMBERSHIP_CATEGORY = 'membership-parents'
PROFESSIONAL_MEMBERSHIP_CATEGORY = 'membership-professionals'
ORGANIZATION_MEMBERSHIP_CATEGORY = 'membership-organizations'
CORPORATE_MEMBERSHIP_CATEGORY = 'membership-corporate'
EMPLOYEE_MEMBERSHIP_CATEGORY = 'membership-corporate-employee'


########################
# Server email         #
########################

SERVER_EMAIL = 'bccf@bccf-staging.bjola.ca'
ADMIN_EMAIL = 'admin_bccf@bccf-staging.bjola.ca'


##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

##################
## OWN SETTINGS ##
##################
import datetime

COMMENTS_USE_RATINGS = False

BCCF_RESOURCE_TYPES = '(article|downloadableform|magazine|tipsheet|video)'
BCCF_SPECIAL_PAGES = ['trainings','resources','tag','programs']
BCCF_CORE_PAGES = ['trainings','resources','tag','programs','blog','news']
SEARCH_MODEL_CHOICES = (
    'bccf.BCCFChildPage',
    'bccf.BCCFTopic',
    'bccf.BCCFPage',
)

# CKEditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbarGroups':  [
            { 'name': 'clipboard',   'groups': [ 'clipboard', 'undo' ] },
            { 'name': 'editing',     'groups': [ 'find', 'selection', 'spellchecker' ] },
            { 'name': 'links' },
            { 'name': 'insert' },
            { 'name': 'forms' },
            { 'name': 'tools' },
            { 'name': 'document',       'groups': [ 'mode', 'document', 'doctools' ] },
            { 'name': 'others' },
            '/',
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ] },
            { 'name': 'paragraph',   'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
            { 'name': 'styles' },
            { 'name': 'colors' },
            { 'name': 'about' }
        ],
        'width': '100%',
        'height': 300,
        'allowedContent': True,
    },
    'basic': {
        'toolbar': 'Basic',
        'toolbarGroups': [
           # { 'name': 'clipboard',   'groups': [ 'clipboard', 'undo' ] },
           # { 'name': 'editing',     'groups': [ 'find', 'selection', 'spellchecker' ] },
            { 'name': 'links' },
           # { 'name': 'insert' },
           # { 'name': 'forms' },
           # { 'name': 'tools' },
           # { 'name': 'document',       'groups': [ 'mode', 'document', 'doctools' ] },
           # { 'name': 'others' },
           # '/',
            { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ] },
           # { 'name': 'paragraph',   'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
           # { 'name': 'styles' },
           # { 'name': 'colors' },
           # { 'name': 'about' }
        ],
        'width': '100%',
        'height': 300,
        'allowedContent': True,
    }
}
RICHTEXT_WIDGET_CLASS = 'ckeditor.widgets.CKEditor'