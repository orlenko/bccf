import logging

from mezzanine import template
from pybb.models import Topic, Post
from django.template.loader import get_template
from django.template.context import Context


log = logging.getLogger(__name__)


register = template.Library()


@register.render_tag
def forum_posts_for_moderation(context, token):
    log.debug('Getting moderation lists...')
    posts = []
    topics = []
    try:
        user = context['request'].user
        profile = user.profile
        if profile and profile.is_forum_moderator:
            posts = Post.objects.filter(on_moderation=True)
            topics = Topic.objects.filter(on_moderation=True)
        context['posts'] = posts
        context['topics'] = topics
        log.debug('%s and %s' % (len(posts), len(topics)))
    except:
        log.debug('Failed to generate moderation lists', exc_info=1)
    t = get_template('bccf/forum_posts_for_moderation.html')
    return t.render(Context(context))