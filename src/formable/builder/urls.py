from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('formable.builder.views',
    url('^save/$', 'save_structure', name='formable-save-structure'),
    url('^submit/$', 'submit_form', name='formable-submit-form'),
    url('^publish/$', 'publish_form', name='formable-publish-form'),
    url('^clone/$', 'clone_structure', name='formable-clone-structure'),
    url('^create/$', 'create_survey', name='formable-create-survey'),
    url('^view/(?P<slug>.*)/$', 'view', name='formable-view'),
    url('^success/$', TemplateView.as_view(template_name="success.html")),
    
    # Added for testing purposes, will be removed after full integration
    url('^test/', TemplateView.as_view(template_name="test/test.html")),
)
