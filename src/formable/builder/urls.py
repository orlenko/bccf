from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from formable.builder import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'formable.views.home', name='home'),
    # url(r'^formable/', include('formable.foo.urls')),
    url('^save/$', views.save_structure, name='save-structure'),
    url('^submit/$', views.submit_form, name='submit-form'),
    url('^publish/$', views.publish_form, name='publish-form'),
    url('^clone/$', views.clone_structure, name='clone-structure'),
    url('^view/(?P<id>\d+)', views.view, name='view'),
    url('^test/', TemplateView.as_view(template_name="test/test.html")),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
