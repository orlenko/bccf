from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.models import NewsPost
from django.template.context import RequestContext
import datetime


def newspost(request, news):
    newspost = get_object_or_404(NewsPost, slug=news)
    page = newspost
    current_item = page.title
    context = RequestContext(request, locals())
    return render_to_response('pages/newspost.html', {}, context_instance=context)