from django.contrib.syndication.views import Feed

from bccf.models import Event



class MemberEventsFeedBase(Feed):
    entity_type = None

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content



class EventsForParentsFeed(MemberEventsFeedBase):
    title = "Events for Parents"
    link = "/events/feed/parents"
    description = "Updates on changes and additions to events for parents."
    entity_type = Event

    def items(self):
        return self.entity_type.objects.filter(page_for='parent').order_by('-date_start')[:25]


class EventsForProfessionalsFeed(MemberEventsFeedBase):
    title = "Events for Professionals"
    link = "/events/feed/professionals"
    description = "Updates on changes and additions to events for professionals."
    entity_type = Event

    def items(self):
        return self.entity_type.objects.filter(page_for='professional').order_by('-date_start')[:25]
