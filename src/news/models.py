from django.conf import settings
from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, RichText
from mezzanine.pages.fields import MenusField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from bccf.models import BCCFChildPage


class DummyTable(models.Model):
    pass

def DummyEmptyResultSet():
    return DummyTable.objects.filter(pk=-1)


class NewsPost(BCCFChildPage):
    class Meta:
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'