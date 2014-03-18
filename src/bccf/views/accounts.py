import logging
log = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from bccf import forms
from bccf.util.memberutil import get_upgrades

def signup(request):
    form = forms.CreateAccountForm()
    
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
    profile = user.profile
    photo_form = forms.PhotoForm()
    order = profile.membership_order
    membership = profile.membership_product_variation
    expiration = profile.membership_expiration_datetime
    upgrades = get_upgrades(membership)    
    
    if not membership:
        from cartridge.shop.models import ProductVariation
        from cartridge.shop.utils import recalculate_cart
        """
        Add free membership depending on their type to cart and redirect to checkout
        """
        sku = 99
        if profile.is_parent:
            sku = 98
        variation = ProductVariation.objects.get(sku=sku)
        request.cart.add_item(variation, 1)
        recalculate_cart(request)
        return redirect('/shop/checkout')

    if request.method == 'POST':
        if 'update-photo' in request.POST:
           photo_form = forms.PhotoForm(request.POST, request.FILES, instance=profile)
           if photo_form.is_valid():
                user = photo_form.save()
                success(request, 'Photo Updated Successfully')
           photo_form = forms.PhotoForm()
        else:
            if tab == 'account':
                form = forms.AccountInformationForm(request.POST, instance=user)
            elif tab == 'contact':
                form = forms.ContactInformationForm(request.POST, instance=profile)
            elif tab == 'profile':
                form = forms.ProfessionalProfileForm(request.POST, instance=profile)
            elif tab == 'social':
                form = forms.SocialMediaForm(request.POST, instance=profile)
            elif tab == 'preferences':
                form = forms.AccountPreferenceForm(request.POST, instance=profile)
            if form.is_valid():
                user = form.save()
                success(request, 'Account Updated Successfully')
            else:
                error(request, 'Please fix the form errors below')
            
    context = RequestContext(request, locals())
    return render_to_response('accounts/accounts_base_profile_update.html', {}, context)