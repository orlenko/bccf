import logging
log = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from bccf import forms

def signup(request):
    form = CreateAccountForm()
    
    if request.method == 'POST':
        form = forms.CreateAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success(request, 'User created, check your email and spam for the account activation email')
            return redirect('/') 
    
    context = RequestContext(request, locals())
    return render_to_response('accounts/account_signup.html', {}, context)

@login_required    
def profile_update(request, tab='home'):
    user = request.user
    photo_form = forms.PhotoForm()
    
    if request.method == 'POST':
        if 'update-photo' in request.POST:
           photo_form = forms.PhotoForm(request.POST, request.FILES, instance=user.profile)
           if photo_form.is_valid():
                user = photo_form.save()
                success(request, 'Photo Updated Successfully');
           photo_form = forms.PhotoForm()
        else:
            if tab == 'account':
                form = forms.AccountInformationForm(request.POST, instance=user)
            elif tab == 'contact':
                form = forms.ContactInformationForm(request.POST, instance=user.profile)
            if form.is_valid():
                user = form.save()
                success(request, 'Account Updated Successfully');
            
    context = RequestContext(request, locals())
    return render_to_response('accounts/accounts_base_profile_update.html', {}, context)