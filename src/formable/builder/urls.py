from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from formable.builder import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'formable.views.home', name='home'),
    # url(r'^formable/', include('formable.foo.urls')),
    url('^build/(?P<id>\d+)*$', views.build, name='build'),
    url('^save/$', views.save_structure, name='save-structure'),
    url('^save/form/$', views.save_form, name='save-form'),
    url('^delete/$', views.delete, name='delete'),
    url('^view/(?P<id>\d+)', views.view, name='view'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
