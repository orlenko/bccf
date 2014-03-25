import logging
log = logging.getLogger(__name__)

from django.template.context import Context
from django.template.loader import get_template

from mezzanine import template

from bccf import forms

register = template.Library()

@register.render_tag
def tab_content(context, token):
    tab = context['tab']
    user = context['user']
    t = get_template('accounts/account_profile_update_%s.html' % tab)

    if 'form' in context and context['form']:
        return t.render(Context(context))
    if tab == 'account':
        context['form'] = forms.AccountInformationForm(instance=user, initial={'postal_code':user.profile.postal_code})
    elif tab == 'contact':
        context['form'] = forms.ContactInformationForm(instance=user.profile)
    elif tab == 'profile':
        context['form'] = forms.ProfessionalProfileForm(instance=user.profile)
    elif tab == 'social':
        context['form'] = forms.SocialMediaForm(instance=user.profile)
    elif tab == 'preferences':
        context['form'] = forms.AccountPreferencesForm(instance=user.profile)
    elif tab == 'forum':
        context['form'] = forms.ForumPreferencesForm(instance=user.profile)
    elif tab == 'adduser':
        context['form'] = forms.AddUserForm(initial={'organization':user, 'membership_type':'professional'})
    return t.render(Context(context))