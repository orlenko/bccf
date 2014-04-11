import logging
log = logging.getLogger(__name__)

from mezzanine import template

register = template.Library()

@register.inclusion_tag("includes/sub-pages/sub_page_podcast.html", takes_context=True)
def podcast_for(context, obj):
    """
    If object is a podcast, show an HTML5 audio tag.
    """
    if obj._meta.object_name == "BCCFChildPage":
        if obj.content_model == "podcast":
            context["podcast_obj"] = obj.get_content_model()
    return context