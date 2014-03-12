import logging
log = logging.getLogger(__name__)

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from bccf.forms import CreateAccountForm

def signup(request):
    form = CreateAccountForm()
    
    if request.method == 'POST':
        form = CreateAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #redirect to success page    
    
    context = RequestContext(request, locals())
    return render_to_response('accounts/account_signup.html', {}, context)