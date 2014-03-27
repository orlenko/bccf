import logging
log = logging.getLogger(__name__)

from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

#Manager
class UserProfileManager(models.Manager):
    def get_directory(self, *args, **kwargs):
        return super(UserProfileManager, self).get_queryset().filter(
            Q(membership_type='professional') | Q(membership_type='organization'),
            Q(show_in_list=True),
        )
    
class ChildPageManager(models.Manager):
           
    def published(self):
        return super(ChildPageManager, self).get_queryset().filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED)
        )           
        
    def by_gparent(self, gparent):
        return self.published().filter(gparent=gparent)
        
    def by_topic(self, topic):
        return self.published().filter(bccf_topic=topic)
        
    def featured(self):
        return self.published().filter(featured=True)
    
class EventManager(ChildPageManager):

    def parent_events(self):
        return self.get_queryset().filter(page_for='parent')
       
    def professional_events(self):
        return self.get_queryset().filter(page_for='professional')    
    
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

class TagManager(ChildPageManager):
        
    def get_queryset(self):
        return super(ChildPageManager, self).get_queryset().filter(
            Q(content_model='topic') | Q(content_model='formpublished') | Q(content_model='campaign')
        )        
        
    def talks(self):
        return super(TagManager, self).published().filter(
            Q(content_model='topic')        
        )
        
    def acts(self):
        return super(TagManager, self).published().filter(
            Q(content_model='formpublished')        
        )
        
    def gets(self):
        return super(TagManager, self).published().filter(
            Q(content_model='campaign')        
        )