import logging
log = logging.getLogger(__name__)

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import success, error
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.template.response import TemplateResponse

from cartridge.shop.models import ProductVariation
from cartridge.shop.utils import recalculate_cart

from bccf_mc.utils import subscribe, unsubscribe, ping

from bccf import forms as f
from bccf.util.memberutil import get_upgrades
from bccf.util.emailutil import send_welcome, send_moderate, send_welcome
from bccf.views.member import membership_upgrade

@sensitive_post_parameters()
@csrf_protect
@never_cache
def my_login(request, template_name='accounts/account_login.html',#'registration/login.html',
          redirect_field_name='next',
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
              
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, reverse('update')))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'title': 'Login',
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def signup(request):
    # Optional queries
    membership_type = request.GET.get('type', None)
    membership_level = request.GET.get('level', None)
    payment_frequency = request.GET.get('freq', None)
    
    form = f.CreateAccountForm(initial={'membership_type': membership_type,
        'membership_level': membership_level, 'payment_frequency': payment_frequency})
    
    if request.method == 'POST':
        form = f.CreateAccountForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            response = redirect('update')
            if form.cleaned_data.get('membership_level') != 'A' and form.cleaned_data.get('membership_type') != 'parent':
                """
                If SKU exists in the query string and the SKU fits with the membership type, 
                add that product to the cart and redirect the user to the checkout
                """
                membership_type = form.cleaned_data.get('membership_type')[:3].upper()
                sku = '%s-%s-%s' % (membership_type, form.cleaned_data.get('membership_level'), form.cleaned_data.get('payment_frequency'))
                variation = ProductVariation.objects.get(sku=sku)
                request.cart.add_item(variation, 1)
                recalculate_cart(request)
                response = redirect('shop_checkout')
            form.save()
            
            subscribe(request, 'af67fb20e3', form.cleaned_data.get('email')) # Members list
            
            if form.cleaned_data.get('in_mailing_list'):
                subscribe(request, '8aebc01ca2', form.cleaned_data.get('email')) # News Letter
            
            new_user = authenticate(username=form.cleaned_data.get('username'), 
                                    password=form.cleaned_data.get('password1'))
            auth_login(request, new_user)
            
            # Send welcome message
            send_welcome(new_user)
            send_moderate("New user signed up.", context={'user': new_user})
            
            success(request, 'User created successfully! Welcome to the BCCF community %s' % form.instance.get_full_name())
            return response
    
    context = RequestContext(request, locals())
    return render_to_response('accounts/account_signup.html', {}, context)

@csrf_protect
def membership_voting(request, type):
    variation = ProductVariation.objects.get(sku=type)
    request.cart.add_item(variation, 1)
    recalculate_cart(request)
    response = redirect('shop_checkout')
    return response

@sensitive_post_parameters()
@csrf_protect
@login_required    
def profile_update(request, tab='home'):
    user = request.user
    profile = user.profile
    photo_form = f.PhotoForm()
    order = profile.membership_order
    membership = profile.membership_product_variation
    expiration = profile.membership_expiration_datetime
            
    page = request.GET.get('page', 1)

    if tab == 'orders':
        from cartridge.shop.models import Order
        """
        Grab all the orders that the user has made
        """
        objects = Order.objects.filter(user_id=user.pk)
        orders = get_page(objects, page)
    elif tab == 'home':
        """
        Grabs the proper upgrade products for the current user.
        """
        upgrades = get_upgrades(profile)
    elif tab == 'members':
        """
        Grabs all the members asssociated with this account
        """
        objects = User.objects.filter(profile__organization=profile)
        members = get_page(objects, page)
    elif tab == 'attending':
        from bccf.models import EventRegistration
        """
        Grabs all the events the user is registered for.
        """
        objects = EventRegistration.objects.filter(user=user)
        events = get_page(objects, page)

    if request.method == 'POST':
        if 'update-photo' in request.POST:
           photo_form = f.PhotoForm(request.POST, request.FILES, instance=profile)
           if photo_form.is_valid():
                user = photo_form.save()
                success(request, 'Photo Updated Successfully')
           photo_form = f.PhotoForm()
        else:
            if tab == 'account':
                form = f.AccountInformationForm(request.POST, instance=user)
            elif tab == 'contact':
                form = f.ContactInformationForm(request.POST, instance=profile)
            elif tab == 'profile':
                form = f.ProfessionalProfileForm(request.POST, instance=profile)
            elif tab == 'social':
                form = f.SocialMediaForm(request.POST, instance=profile)
            elif tab == 'preferences':
                form = f.AccountPreferencesForm(request.POST, instance=profile)
            elif tab == 'forum':
                form = f.ForumPreferencesForm(request.POST, request.FILES, instance=profile)
            elif tab == 'adduser':
                form = f.AddUserForm(request.POST)
            elif tab == 'register':
                form = f.RegisterUserForm(request, data=request.POST)
                request.session['register_selected_members'] = request.POST.getlist('members')
                request.session['register_selected_event'] = request.POST.get('event')
                return redirect(reverse('register-event'))
            elif tab == 'affiliation':
                form = f.AffiliationForm(request.POST, instance=profile)
                print profile.membership_level
                print request.POST.get('membership_level')
                membership_upgrade(request, request.POST.get('membership_level'))
            if form.is_valid():
                ping()
                user = form.save()
                success(request, 'Account Updated Successfully')
                if tab == 'preferences':
                    if form.cleaned_data.get('in_mailing_list'):
                        subscribe(request, '8aebc01ca2', request.user.email) # News letter
                    else:
                        unsubscribe(request, '8aebc01ca2', request.user.email)
                        
                elif tab == 'adduser':
                    form = None
            else:
                error(request, 'Please fix the form errors below')
            
    context = RequestContext(request, locals())
    return render_to_response('accounts/accounts_base_profile_update.html', {}, context)

@login_required
def register_event(request):
    """
    Registers users to the event, registerer must complete registration using checkout if
    the event is not free
    """
    from cartridge.shop.utils import recalculate_cart
    from bccf.models import Event, EventRegistration
    
    member_ids = request.session['register_selected_members']
    event_id = request.session['register_selected_event']
    response = redirect(reverse('update'))
    message = 'Users registered successfully.'

    event = Event.objects.get(id=event_id)
    seats = len(EventRegistration.objects.filter(event=event)) + len(member_ids)
    
    if event.max_seats < seats: # Not everyone will fit
        error(request, 'There is not enough space in the event for your members.')
        return response
    
    if event.event_product: # If paid event, add event to cart
        variation = ProductVariation.objects.get(sku='EVENT-%s' % event.pk)
        request.cart.add_item(variation, len(member_ids))
        recalculate_cart(request)
        response = redirect('/shop/checkout')
        message = 'Users registered successfully. Please continue with the  checkout to complete registrations.'
        
        # Send event registration confirmation
        send_reminder("Event Registration Pending.", request.user, context={'event':event})
        
    else: # If not paid event, auto-register the members
        members = []        
        for member_id in member_ids:
            user = User.objects.get(id=member_id)
            members.append(user)
            EventRegistration.objects.create(user=user, event=event)
            send_reminder("Event Registration Complete.", user, context={'event': event})
          
        # Send event registration confirmation
        send_reminder("Event Registration Complete.", request.user, context={'event': event, 'members': members})

        # Delete session variables since the IDs have been registered
        del request.session['register_selected_members']
        del request.session['register_selected_event']   

    success(request, message)
    return response

def get_page(objects, page):
    """
    Helper function for pagination.
    """
    p = Paginator(objects, 10)
    try:
        objects = p.page(page)
    except PageNotAnInteger:
        objects = p.page(1)
    except EmptyPage:
        objects = p.page(p.num_pages)
    return objects
