from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context import RequestContext
from bccf.models import EventForParents
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def parents_page(request, slug=None):
    user = request.user
    authenticated = user and not user.is_anonymous()
    profile = None
    membership_product = None
    if authenticated:
        profile = user.profile
        if profile:
            membership_product = profile.membership_product_variation
    queryset = EventForParents.objects.all()  # @UndefinedVariable
    paginator = Paginator(queryset, 6)
    pagenum = request.GET.get('page')
    try:
        events = paginator.page(pagenum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events  = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)
    context = RequestContext(request, locals())
    return render_to_response('bccf/parents_page.html', {}, context_instance=context)
