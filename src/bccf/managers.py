import logging
log = logging.getLogger(__name__)

from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

#Manager
class UserProfileManager(models.Manager):
    def get_directory(self, *args, **kwargs):
        return super(UserProfileManager, self).get_queryset().filter(
            ~Q(user__is_staff=True), ~Q(user__is_superuser=True),
            Q(membership_type='professional') | Q(membership_type='organization'),
            Q(show_in_list=True),
        )
    
class ChildPageManager(DisplayableManager):     
        
    def __init__(self, *args, **kwargs):
        super(ChildPageManager, self).__init__(*args, **kwargs)

    def by_gparent(self, gparent):
        return self.published().filter(gparent=gparent)
        
    def by_topic(self, topic):
        return self.published().filter(bccf_topic=topic)
        
    def by_program(self, program):
        return self.published().filter(bccf_program=program)
        
    def featured(self):
        return self.published().filter(featured=True)
    
class EventManager(ChildPageManager):

    def __init__(self, *args, **kwargs):
        super(EventManager, self).__init__(*args, **kwargs)   
    
    def need_reminder(self):
        last_month = now() + relativedelta(weeks=4)
        limit = now() + relativedelta(weeks=2)
        return super(EventManager, self).get_queryset().filter(
            Q(date_start__lte=last_month), Q(date_start__gte=limit),
            ~Q(event_product=None)
        )

    def need_freeing(self):
        limit = now() + relativedelta(weeks=2)
        return super(EventManager, self).get_queryset().filter(
            Q(date_start__lte=limit), Q(date_start__gte=now()),
            ~Q(event_product=None)
        )
        
    def user_event_list(self, user):
        return self.published().filter(
            Q(date_start__gte=now()), provider=user        
        )

class TagManager(ChildPageManager):
        
    def __init__(self, *args, **kwargs):
        super(TagManager, self).__init__(*args, **kwargs)
