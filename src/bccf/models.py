from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=255)
    star_blog_id = models.IntegerField(null=True, blank=True)
    star_survey_id = models.IntegerField(null=True, blank=True)
    star_forum_post_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class TopicLink(models.Model):
    topic = models.ForeignKey(Topic)
    model_name = models.CharField(max_length=255)
    entity_id = models.IntegerField()

    @property
    def target(self):
        return globals()[self.model_name].objects.get(pk=self.entity_id)

    def __unicode__(self):
        return '%s - %s' % (self.topic.name, self.target)
