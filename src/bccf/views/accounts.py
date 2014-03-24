import logging
log = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from cartridge.shop.models import ProductVariation

from bccf import forms
from bccf.util.memberutil import get_upgrades

def signup(request):
    # Optional queries
    membership_type = request.GET.get('type', None)
    product_sku = request.GET.get('var', None)
    
    if product_sku and not ProductVariation.objects.filter(sku=product_sku).exists():
        raise Http404
    
    form = forms.CreateAccountForm(initial={'membership_type': membership_type})
    
    if request.method == 'POST':
        form = forms.CreateAccountForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            response = redirect('update')
            if product_sku and membership_type == form.cleaned_data.get('membership_type'):
                """
                If SKU exists in the query string and the SKU fits with the membership type, 
                add that product to the cart and redirect the user to the checkout
                """
                from cartridge.shop.utils import recalculate_cart
                variation = ProductVariation.objects.get(sku=product_sku)
                request.cart.add_item(variation, 1)
                recalculate_cart(request)
                response = redirect('shop_checkout')
            form.save()
            new_user = authenticate(username=form.cleaned_data.get('username'), 
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            success(request, 'User created successfully! Welcome to the BCCF community %s' % form.instance.get_full_name())
            return response
    
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
    
    if 'addmembers' in request.session:
        try:
            new_users, new_user_errors = request.session.pop('addmembers')
            feedback = {
                'new_users': new_users,
                'new_user_errors': new_user_errors
            }
        except:
            pass

    if tab == 'orders':
        from cartridge.shop.models import Order
        """
        Grab all the orders that the user has made
        """
        orders = Order.objects.filter(user_id=user.pk)

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
            elif tab == 'forum':
                form = forms.ForumPreferencesForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                user = form.save()
                success(request, 'Account Updated Successfully')
            else:
                error(request, 'Please fix the form errors below')
            
    context = RequestContext(request, locals())
    return render_to_response('accounts/accounts_base_profile_update.html', {}, context)