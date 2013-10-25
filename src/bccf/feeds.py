from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from bccf.models import EventForParents


class EventsForParentsFeed(Feed):
    title = "Events for Parents"
    link = "/parents/event/feed/"
    description = "Updates on changes and additions to events for parents."

    def items(self):
        return EventForParents.objects.order_by('-date_start')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
