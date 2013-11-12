from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('formable.builder.views',
    url('^save/$', 'save_structure', name='save-structure'),
    url('^submit/$', 'submit_form', name='submit-form'),
    url('^publish/$', 'publish_form', name='publish-form'),
    url('^clone/$', 'clone_structure', name='clone-structure'),
    url('^view/(?P<id>\d+)', 'view', name='view'),
    
    # Added for testing purposes, will be removed after full integration
    url('^test/', TemplateView.as_view(template_name="test/test.html")),
)
