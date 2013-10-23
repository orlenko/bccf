from django.shortcuts import render_to_response
from django.template.context import RequestContext

from bccf.models import EventForParents
from bccf.util.membership import require_parent
from django.views.decorators.cache import never_cache


def parents_event(request, slug):
    event = EventForParents.objects.get(slug=slug)  # @UndefinedVariable get
    context = RequestContext(request, locals())
    return render_to_response('bccf/event.html', {}, context_instance=context)


@require_parent
@never_cache
def parents_event_signup(request, slug):
    event = EventForParents.objects.get(slug=slug)  # @UndefinedVariable get
    context = RequestContext(request, locals())
    return render_to_response('bccf/event_signup.html', {}, context_instance=context)
