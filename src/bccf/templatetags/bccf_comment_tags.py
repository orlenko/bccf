import logging
log = logging.getLogger(__name__)

from django.contrib.auth.models import User

from mezzanine import template

register = template.Library()

@register.inclusion_tag("generic/includes/comment/comment.html", takes_context=True)
def comment_for(context, obj):
    try:
        user = User.objects.get(email=obj.email)
        context['comment_obj'] = obj
        context['comment_user'] = user
        context['comment_profile'] = user.profile
    except Exception:
        return context
    return context

