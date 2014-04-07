import mailchimp
import logging

log = logging.getLogger(__name__)

from django.contrib import messages

def get_mailchimp_api():
    """
    Creates a new mailchimp api object.
    """
    return mailchimp.Mailchimp('b560f8c78c968b043d31ab244f69ac42-us3')
    
def ping():
    try:
        m = get_mailchimp_api()
        m.helper.ping()
    except:
        log.debug('Invalid API Key')    
    
def subscribe(request, list_id, email):
    try:
        m = get_mailchimp_api()
        m.lists.subscribe(list_id, {'email':email})
        messages.success(request, 'Successfully added to mailing list, please confirm the addition.')
    except mailchimp.ListAlreadySubscribedError:
        messages.error(request, 'The email is already subscribed to the list')
    except mailchimp.Error, e:
        messages.error(request, 'An error occurred: %s - %s' % (e.__class__, e))
    
def unsubscribe(request, list_id, email):
    try:
        m = get_mailchimo_api()
        m.lists.unsubscribe(list_id, {'email':email})
        messages.success(request, 'Successfully removed from the mailing list.')
    except mailchimp.Error, e:
        messages.error(request, 'An error occurred: %s - %s' % (e.__class__, e))