import logging

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.db.models import ObjectDoesNotExist

from bccf.models import Topic

log = logging.getLogger(__name__)

def topic_page(request, topic):
    page = Topic.objects.get(slug=topic)
    context = RequestContext(request, locals())
    return render_to_response('bccf/bccf_page.html', {}, context_instance=context)