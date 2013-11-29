from datetime import timedelta

from django.contrib.messages import error
from django.core.urlresolvers import reverse
from django.db.models import get_model, ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

import logging
log = logging.getLogger(__name__)

try:
    from json import dumps
except ImportError:
    from django.utils.simplejson import dumps

from bccf.forms import BCCFRatingForm
from bccf.models import Topic, EventForParents, EventForProfessionals
from news.models import NewsPost

from mezzanine.conf import settings
from mezzanine.utils.cache import add_cache_bypass
from mezzanine.utils.views import set_cookie

def home(request):
    topics = Topic.objects.all();
    pastThirtyDays = timezone.now().date() + timedelta(days=30)
    eventForParents = EventForParents.objects.filter(date_start__gte=timezone.now().date(), date_start__lte=pastThirtyDays)
    eventForProfessionals = EventForProfessionals.objects.filter(date_start__gte=timezone.now().date(), date_start__lte=pastThirtyDays)
    
    log.info(pastThirtyDays)
    log.info(eventForParents)
    
    context = RequestContext(request, locals())
    return render_to_response('index.html', {}, context_instance=context);
    pass

def initial_validation(request, prefix):
    """
    Returns the related model instance and post data to use in the
    comment/rating views below.

    Both comments and ratings have a ``prefix_ACCOUNT_REQUIRED``
    setting. If this is ``True`` and the user is unauthenticated, we
    store their post data in their session, and redirect to login with
    the view's url (also defined by the prefix arg) as the ``next``
    param. We can then check the session data once they log in,
    and complete the action authenticated.

    On successful post, we pass the related object and post data back,
    which may have come from the session, for each of the comments and
    ratings view functions to deal with as needed.
    """
    post_data = request.POST
    settings.use_editable()
    login_required_setting_name = prefix.upper() + "S_ACCOUNT_REQUIRED"
    posted_session_key = "unauthenticated_" + prefix
    redirect_url = ""
    if getattr(settings, login_required_setting_name, False):
        if not request.user.is_authenticated():
            request.session[posted_session_key] = request.POST
            error(request, _("You must logged in. Please log in or "
                             "sign up to complete this action."))
            redirect_url = "%s?next=%s" % (settings.LOGIN_URL, reverse(prefix))
        elif posted_session_key in request.session:
            post_data = request.session.pop(posted_session_key)
    if not redirect_url:
        try:
            model = get_model(*post_data.get("content_type", "").split(".", 1))
            if model:
                obj = model.objects.get(id=post_data.get("object_pk", None))
        except (TypeError, ObjectDoesNotExist):
            redirect_url = "/"
    if redirect_url:
        if request.is_ajax():
            return HttpResponse(dumps({"location": redirect_url}))
        else:
            return redirect(redirect_url)
    return obj, post_data

def rating(request):
    """
    Handle a ``RatingForm`` submission and redirect back to its
    related object.
    """
    response = initial_validation(request, "rating")
    if isinstance(response, HttpResponse):
        return response
    obj, post_data = response
    url = add_cache_bypass(obj.get_absolute_url().split("#")[0])
    response = redirect(url + "#rating-%s" % obj.id)
    rating_form = BCCFRatingForm(request, obj, post_data)
    if rating_form.is_valid():
        rating_form.save()
        if request.is_ajax():
            # Reload the object and return the rating fields as json.
            obj = obj.__class__.objects.get(id=obj.id)
            rating_name = obj.get_ratingfield_name()
            json = {}
            for f in ("average", "count", "sum"):
                json["rating_" + f] = getattr(obj, "%s_%s" % (rating_name, f))
            response = HttpResponse(dumps(json))
        ratings = ",".join(rating_form.previous + [rating_form.current])
        set_cookie(response, "mezzanine-rating", ratings)
    return response
