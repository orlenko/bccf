from django.utils.timezone import now
from django.db import models
from django.db.models import Q

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

#Manager
class ChildPageManager(models.Manager):
    
    def get_queryset(self):
        return super(ChildPageManager, self).get_queryset().filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED)
        )         
        
    def by_gparent(self, gparent):
        return self.get_queryset().filter(gparent=gparent)
        
    def by_topic(self, topic):
        return self.get_queryset().filter(bccf_topic=topic)
        
    def featured(self):
        return self.get_queryset().filter(featured=True)
    
class EventManager(ChildPageManager):

    def parent_events(self):
        return self.get_queryset().filter(page_for='parent')
       
    def professional_events(self):
        return self.get_queryset().filter(page_for='professional')    
    
class TagManager(ChildPageManager):
        
    def get_queryset(self):
        return super(ChildPageManager, self).get_queryset().filter(
            Q(content_model='topic') | Q(content_model='formpublished') | Q(content_model='campaign')
        )        
        
    def talks(self):
        return super(TagManager, self).get_queryset().filter(
            Q(content_model='topic')        
        )
        
    def acts(self):
        return super(TagManager, self).get_queryset().filter(
            Q(content_model='formpublished')        
        )
        
    def gets(self):
        return super(TagManager, self).get_queryset().filter(
            Q(content_model='campaign')        
        )