from django.contrib.syndication.views import Feed

from bccf.models import EventForParents, EventForProfessionals



class MemberEventsFeedBase(Feed):
    entity_type = None

    def items(self):
        return self.entity_type.objects.order_by('-date_start')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content



class EventsForParentsFeed(MemberEventsFeedBase):
    title = "Events for Parents"
    link = "/parents/event/feed/"
    description = "Updates on changes and additions to events for parents."
    entity_type = EventForParents


class EventsForProfessionalsFeed(MemberEventsFeedBase):
    title = "Events for Professionals"
    link = "/professionals/event/feed/"
    description = "Updates on changes and additions to events for professionals."
    entity_type = EventForProfessionals
