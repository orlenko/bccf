
from django.conf.urls.defaults import *

urlpatterns = patterns("bccf_form_builder.forms.views",
    url(r"(?P<slug>.*)/sent/$", "form_sent", name="form_sent"),
    url(r"(?P<slug>.*)/$", "form_detail", name="form_detail"),
)
