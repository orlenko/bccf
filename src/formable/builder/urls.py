from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('formable.builder.views',
    url('^publish/(?P<id>.+)$', 'publish_form', name='formable-publish-form'),
    url('^create/(?P<type>.+)/(?P<id>.+)/$', 'create_survey', name='formable-edit-clone-form'),
    url('^create/$', 'create_survey', name='formable-create-form'),
    url('^view/(?P<slug>.+)/$', 'view', name='formable-view'),
    
    # Added for testing purposes, will be removed after full integration
    url('^test/', TemplateView.as_view(template_name="test/test.html")),
)
