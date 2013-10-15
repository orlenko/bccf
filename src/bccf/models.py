from django.db import models
from django.contrib.auth.models import User



class Topic(models.Model):
    name = models.CharField(max_length=255)
    star_blog_id = models.IntegerField(null=True, blank=True)
    star_survey_id = models.IntegerField(null=True, blank=True)
    star_forum_post_id = models.IntegerField(null=True, blank=True)


class TopicLink(models.Model):
    topic = models.ForeignKey(Topic)
    model_name = models.CharField(max_length=255)
    entity_id = models.IntegerField()


RATINGS = [(str(i), i) for i in range(1, 6)]

class Rating(models.Model):
    model_name = models.CharField(max_length=255)
    entity_id = models.IntegerField()
    rated_by = models.ForeignKey(User)
    rated_on = models.DateTimeField(auto_now_add=True, blank=True)
    rating = models.IntegerField(choices=RATINGS)
