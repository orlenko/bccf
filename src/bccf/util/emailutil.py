import logging
from bccf.models import EmailLog
log = logging.getLogger(__name__)

from django.db.models.loading import get_model
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

from mezzanine.utils.email import send_mail_template

from bccf.models import Event, EventRegistration, Settings
from cartridge.shop.models import Order

TEMPLATE_DIR = "email/%s"
NO_EMAIL = Settings.get_setting('NO_REPLY_EMAIL')
MOD_EMAIL = Settings.get_setting('MODERATOR_EMAIL')


def send_email(fr, to, subject, plain, html=None):
    msg = EmailMultiAlternatives(subject, plain, fr, [to])
    if html:
        msg.attach_alternative(html, "text/html")
    if EmailLog.can_send(to, subject, plain, html):
        msg.send()
        EmailLog.on_send(to, subject,  plain, html)


def send_welcome(user, subject="Welcome to BCCF", fr=NO_EMAIL, template="email_welcome.txt", template_html="email_welcome.html"):
    """
    Helper function that sends a welcome email to users upon registration.
    """
    to = user.email
    c = Context({'user': user})
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template_html, {}, context_instance=c)
    send_email(fr, to, subject, plain_content, html_content)


def send_moderate(subject, context={}, to=MOD_EMAIL, fr=NO_EMAIL,
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
    c = Context(context)
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template_html, {}, context_instance=c)
    send_email(fr, to, subject, plain_content, html_content)


def send_reminder(subject, user, context={}, fr=NO_EMAIL, template="email_remind.txt",
    template_html="email_remind.html"):
    """
    Helper function that sends an email when something needs reminding.
    Things that need reminding include
        - expiring membership,
        - membership expired,
        - event payment,
        - event seat released,
    """
    to = user.email
    c = Context(context)
    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
    html_content = render_to_string(TEMPLATE_DIR % template_html, {}, context_instance=c)
    send_email(fr, to, subject, plain_content, html_content)


# def send_receipt(request, user, order, fr=NO_EMAIL):
#    """
#    Helper function that sends an receipt to the user who bought a product
#    from the BCCF Shop
#    """
#    to = user.email
#    c = Context({'order': order, 'user': user})
#    plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
#    html_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
#
#    msg = EmailMultiAlternatives(subject, plain_content, fr, [to])
#    msg.attach_alternative(html_content, "text/html")
#    msg.send()

def send_after_survey(request, id, fr=NO_EMAIL):
    """
    Helper function that sends a link to the after survey after the event
    has finished.

    THIS IS BROKEN!
    """
    return
#     to = []
#     event = Event.objects.get(id=id)
#     registrations = EventRegistration.objects.filter(event=event)
#
#     # Grab all the user's emails
#     for regs in registrations:
#         to.append(regs.user.email)
#     c = Context({'event': event, 'user': user})
#     plain_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
#     html_content = render_to_string(TEMPLATE_DIR % template, {}, context_instance=c)
#
#     msg = EmailMultiAlternatives(subject, plain_content, fr, to)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()