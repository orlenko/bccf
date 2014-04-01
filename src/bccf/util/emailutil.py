import logging
log = logging.getLogger(__name__)

from django.db.models.loading import get_model
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

from bccf.models import Event, EventRegistration, Settings
from cartridge.shop.models import Order

TEMPLATE_DIR = "email/%s"
NO_EMAIL = Settings.get_setting('NO_REPLY_EMAIL')
MOD_EMAIL = Settings.get_setting('MODERATOR_EMAIL')
    
def send_welcome(request, subject="Welcome to BCCF", fr=NO_EMAIL, template="email_welcome.txt", template_html="email_welcome.html"):
    """
    Helper function that sends a welcome email to users upon registration.
    """
    to = request.user.email
    c = Context({'user': request.user})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template_html, {}, context_instance=c)
    
    msg = EmailMultiAlternatives(subject, plain_content, fr, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_moderate(request, subject, app_name, model_name, id, to=MOD_EMAIL, fr=NO_EMAIL,
    template="email_moderate.txt", template_html="email_moderate.html"):
    """
    Helper function that sends an email when something needs moderation.
    Things that need moderation include
        - campaign creation,
        - program request,
        - forum post,
        - membership cancellation,
        - new member sign up,
        - and shop orders.
    """
    model = get_model(app_name, model_name)
    object = model.objects.get(id=id)
    c = Context({'obj': object})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template_html, {}, context_instance=c)
    
    msg = EmailMultiAlternatives(subject, plain_content, fr, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_reminder(subject, user, app_name, model_name, id, fr=NO_EMAIL):
    """
    Helper function that sends an email when something needs reminding.
    Things that need reminding include
        - expiring membership,
        - membership expired,
        - event payment,
        - event seat released,
    """
    to = 'khcastillo@hotmail.com' #user.email
    model = get_model(app_name, model_name)
    object = model.objects.get(id=id)
    c = Context({'obj': object, 'user': user})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    
    msg = EmailMultiAlternatives(subject, plain_content, fr, [to])
    msg.attach_alternative(html_content, "text/html")
    # msg.send()
    
    send_mail('Test Email', plain_content, fr, [to], fail_silently=False, html_message=html_content)
    
def send_receipt(request, user, order, fr=NO_EMAIL):
    """
    Helper function that sends an receipt to the user who bought a product
    from the BCCF Shop
    """
    to = user.email
    c = Context({'order': order, 'user': user})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    
    msg = EmailMultiAlternatives(subject, plain_content, fr, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_after_survey(request, id, fr=NO_EMAIL):
    """
    Helper function that sends a link to the after survey after the event
    has finished.
    """
    to = []
    event = Event.objects.get(id=id)
    registrations = EventRegistration.objects.filter(event=event)

    # Grab all the user's emails    
    for regs in registrations:
        to.append(regs.user.email)
    c = Context({'event': event, 'user': user})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    
    msg = EmailMultiAlternatives(subject, plain_content, fr, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()