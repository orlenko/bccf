from django.conf.urls import patterns, include, url
from django.contrib import admin
from bccf import settings
from bccf.feeds import EventsForParentsFeed, EventsForProfessionalsFeed

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

    # FORUM URLs
    (r'^forum/', include('pybb.urls', namespace='pybb')),

    # Cartridge URLs.
    ("^shop/", include("cartridge.shop.urls")),

    # Formable URLs
    ("^formable/", include("formable.builder.urls")),

    # Podcasts
    #('^podcasts/', include('podcasting.urls')),

    url('^bccf_admin_page_ordering/$', 'bccf.views.page.bccf_admin_page_ordering', name='bccf-admin-page-ordering'),

    url("^accounts/update/(?P<tab>.+)/$", "bccf.views.accounts.profile_update", name='update-tab'),
    url("^accounts/update/$", "bccf.views.accounts.profile_update", name='update'),
    url("^accounts/signup/$", "bccf.views.accounts.signup", name='signup'),
    url("^account/orders/$", "cartridge.shop.views.order_history", name="shop_order_history"),

    #Member views
    (r'^member/', include('bccf.member_urls')),

    # Events
    url(r'events/feed/parents/$', EventsForParentsFeed(), name='events-for-parents'),
    url(r'events/feed/professionals/$', EventsForProfessionalsFeed(), name='events-for-professionals'),
    url(r'events/signup/(?P<slug>.*)/$', 'bccf.views.events.signup', name='events-signup'),
    url(r'events/create/$', 'bccf.views.events.create', name='events-create'),
    url(r'events/edit/(?P<slug>.*)/$', 'bccf.views.events.edit', name='events-edit'),
    url(r'events/attendees/(?P<id>.+)/$', 'bccf.views.events.attendees', name='events-attendees'),
    url(r'events/remove/survey/$', 'bccf.views.events.remove_survey', name='events-remove-survey'),
    url(r'events/(?P<slug>.*)/$', 'bccf.views.events.event', name='events-event'),

    # Campaigns
    url(r'campaigns/create/$', 'bccf.views.campaign.create', name='campaigns-create'),
    url(r'campaigns/edit/(?P<slug>.*)/$', 'bccf.views.campaign.edit', name='campaigns-edit'),

    # MEZZANINE URL OVERRIDES
    #------------------------
    # The patterns here will be used to override Mezzanine-specific urls.
    url("^rating/$", "bccf.views.views.rating", name="rating"),

    # Reports
    url(r'^report/survey/event/(?P<slug>.+)/$', 'bccf.views.report.event_survey_report', name='event-survey-report'),
    url(r'^report/survey/(?P<slug>.+)/$', 'bccf.views.report.survey_report', name='survey-report'),

    #Pages
    url(r'^filter/(?P<query>.*)/$', 'bccf.views.page.filter', name='filter'),
    url(r'^next/topic/(?P<topic>.+)/(?P<which>.*)/(?P<offset>\d+)/$', 'bccf.views.page.topic_next', name='topic-next'),
    url(r'^next/(?P<parent>.+)/(?P<which>.*)/(?P<offset>\d+)/$', 'bccf.views.page.next', name='bccf-next'),
    url(r'^topic/(?P<topic>.+)/$', 'bccf.views.page.topic_page', name='topic-page'),
    url(r'^bccf/resources/type/(?P<type>%s)/$' % settings.BCCF_RESOURCE_TYPES, 'bccf.views.page.resource_type_page', name='resource-type'),
    url(r'^bccf/(?P<parent>.+)/(?P<child>.+)/(?P<baby>.+)/$', 'bccf.views.page.page', name='bccf-baby'),
    url(r'^bccf/(?P<parent>.+)/(?P<child>.+)/$', 'bccf.views.page.page', name='bccf-child'),
    url(r'^bccf/(?P<parent>.*)/$', 'bccf.views.page.page', name='page'),

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
