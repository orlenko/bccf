from django.shortcuts import render_to_response
from django.template.context import RequestContext
from bccf.models import Event
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def parents_page(request, slug=None):
    if slug is not None and request.is_ajax():
        """
        We will generate a completely new page with the data we have and send it
        back via ajax to the caller page
        """
        context = RequestContext(request, locals())
        return render_to_response('generic/sub_page_box.html', {}, context_instance=context)
    boxes = [
        {
         'slug':'test',
         'img':'http://placehold.it/100x50/6eb43f/ffffff&text=Placeholder',
         'text':'Product 1'
        },
        {
         'slug':'test2',
         'img':'http://placehold.it/100x50/6eb43f/ffffff&text=Placeholder',
         'text':'Product 2'
        },
        {
         'slug':'test3',
         'img':'http://placehold.it/100x50/6eb43f/ffffff&text=Placeholder',
         'text':'Product 3'
        },
        {
         'slug':'test4',
         'img':'http://placehold.it/100x50/6eb43f/ffffff&text=Placeholder',
         'text':'Product 4'
        },
        {
         'slug':'test5',
         'img':'http://placehold.it/100x50/6eb43f/ffffff&text=Placeholder',
         'text':'Product 5'
        },
    ]
    user = request.user
    authenticated = user and not user.is_anonymous()
    profile = None
    membership_product = None
    if authenticated:
        profile = user.profile
        if profile:
            membership_product = profile.membership_product_variation
    queryset = Event.objects.filter(page_for='parent')
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
