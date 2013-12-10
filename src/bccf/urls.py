
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from mezzanine.core.views import direct_to_template

from bccf import settings
from bccf.feeds import EventsForParentsFeed, EventsForProfessionalsFeed
from bccf.views.events import ProfessionalEventWizard, FORMS


admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = patterns("",

    #UPLOADS
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),

    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),

    (r'^forum/', include('pybb.urls', namespace='pybb')),

    url(r'^news/(?P<news>.*)/$', 'bccf.views.newsposts.newspost', {}, name='news-post'),

    # Cartridge URLs.
    ("^shop/", include("cartridge.shop.urls")),

    # Formable URLs
    ("^formable/", include("formable.builder.urls")),

    # Podcasts
    #('^podcasts/', include('podcasting.urls')),

    url("^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

    url(r'^member/profile/$', 'bccf.views.member.profile', name='member-profile'),
    url(r'^member/membership/upgrade/(?P<product_id>.*)/$', 'bccf.views.member.membership_upgrade', name='member-membership-upgrade'),
    url(r'^member/membership/(?P<slug>.*)/$', 'bccf.views.member.membership', name='member-membership'),

    # Parents
    url(r'^parents/$', 'bccf.views.parents.parents_page', name='parents-page'),
    url(r'^parents/event/feed/', EventsForParentsFeed()),
    url(r'^parents/event/signup/(?P<slug>.*)/$', 'bccf.views.events.parents_event_signup', name='parents-event-signup'),
    url(r'^parents/event/(?P<slug>.*)/$', 'bccf.views.events.parents_event', name='parents-event'),
    url(r'^parents/(?P<slug>.*)/$', 'bccf.views.parents.parents_page', name='parents-ajax-page'),

    # Professionals
    url(r'^professionals/$', 'bccf.views.professionals.professionals_page', name='professionals-page'),
    url(r'^professionals/event/feed/', EventsForProfessionalsFeed()),
    url(r'^professionals/event/signup/(?P<slug>.*)/$', 'bccf.views.events.professionals_event_signup', name='professionals-event-signup'),
    url(r'^professionals/event/create/$', ProfessionalEventWizard.as_view(FORMS), name='professionals-event-create'),
    url(r'^professionals/event/report/(?P<slug>.*)/$', 'bccf.views.events.professional_survey_download_report', name='professional-download-report'),
    url(r'^professionals/event/(?P<slug>.*)/$', 'bccf.views.events.professionals_event', name='professionals-event'),
    
    #Resources
    url(r'^resources/$', 'bccf.views.resources.resources_page', name='resources-page'),
    url(r'^resources/(?P<type>[a-z]+)/', 'bccf.views.resources.resources_page', name='resources-type'),
    
    #Programs
    url(r'^programs/$', 'bccf.views.programs.programs_page', name='programs-page'),

    url(r'^page_test/$', TemplateView.as_view(template_name="bccf/bccf_page.html")),
    
    #AJAX Calls
    url(r'^get/(?P<parent>[a-zA-Z-0-9]+)/(?P<type>[a-zA-Z-0-9]+)/(?P<page>[a-zA-Z-0-9]+)/$', 'bccf.views.ajax.get', name='ajax-page'),
    url(r'^get/(?P<offset>[0-9]+)/(?P<model>[a-zA-Z]+)', 'bccf.views.ajax.add', name='ajax-add'),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^$", 'bccf.views.views.home', name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "/", which
    # is the value used below in the ``{"slug": "/"}`` part.
    # Also note that the normal rule of adding a custom
    # template per page with the template name using the page's slug
    # doesn't apply here, since we can't have a template called
    # "/.html" - so for this case, the template "pages/index.html"
    # should be used if you want to customize the homepage's template.

    # url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    # MEZZANINE URL OVERRIDES
    #------------------------
    # The patterns here will be used to override Mezzanine-specific urls.
    url("^rating/$", "bccf.views.views.rating", name="rating"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns in
    # ``mezzanine.urls``, go right ahead and take the parts you want
    # from it, and use them directly below instead of using
    # ``mezzanine.urls``.
    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # You can also mount all of Mezzanine's urlpatterns under a
    # URL prefix if desired. When doing this, you need to define the
    # ``SITE_PREFIX`` setting, which will contain the prefix. Eg:
    # SITE_PREFIX = "my/site/prefix"
    # For convenience, and to avoid repeating the prefix, use the
    # commented out pattern below (commenting out the one above of course)
    # which will make use of the ``SITE_PREFIX`` setting. Make sure to
    # add the import ``from django.conf import settings`` to the top
    # of this file as well.
    # Note that for any of the various homepage patterns above, you'll
    # need to use the ``SITE_PREFIX`` setting as well.

    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
