from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bccf.models import Page
from django.template.context import RequestContext
import datetime
    
def newspost(request, news=None):
    page = Page.objects.get(slug='news')
    context = RequestContext(request, locals())
    return render_to_response('bccf/news_blog_page.html', {}, context_instance=context)