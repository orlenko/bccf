from django.conf import settings
from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, RichText
from mezzanine.pages.fields import MenusField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from bccf.models import BCCFChildPage, BCCFPage
from bccf.managers import ChildPageManager

class DummyTable(models.Model):
    pass

def DummyEmptyResultSet():
    return DummyTable.objects.filter(pk=-1)


class NewsPost(BCCFChildPage):
    objects = ChildPageManager()
    class Meta:
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'
        
    def __init__(self, *args, **kwargs):
        super(NewsPost, self).__init__(*args, **kwargs)          

    def save(self, **kwargs):
        page = BCCFPage.objects.get(slug='news')
        self.gparent = page
        super(NewsPost, self).save(**kwargs);