import logging
log = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import success, error
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from cartridge.shop.models import ProductVariation

from bccf import forms
from bccf.util.memberutil import get_upgrades
from bccf.util.emailutil import send_welcome, send_moderate, send_welcome

def my_login(request, **kwargs):
     if not request.user.is_authenticated():
         login(request, **kwargs)
     return HttpResponseRedirect(reverse('update'))

def signup(request):
    # Optional queries
    membership_type = request.GET.get('type', None)
    membership_level = request.GET.get('level', None)
    payment_frequency = request.GET.get('freq', None)
    
    form = forms.CreateAccountForm(initial={'membership_type': membership_type,
        'membership_level': membership_level, 'payment_frequency': payment_frequency})
    
    if request.method == 'POST':
        form = forms.CreateAccountForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            response = redirect('update')
            if form.cleaned_data.get('membership_level') != 'A':
                """
                If SKU exists in the query string and the SKU fits with the membership type, 
                add that product to the cart and redirect the user to the checkout
                """
                from cartridge.shop.utils import recalculate_cart
                membership_type = form.cleaned_data.get('membership_type')[:3].upper()
                sku = '%s-%s-%s' % (membership_type, form.cleaned_data.get('membership_level'), form.cleaned_data.get('payment_frequency'))
                variation = ProductVariation.objects.get(sku=sku)
                request.cart.add_item(variation, 1)
                recalculate_cart(request)
                response = redirect('shop_checkout')
            form.save()
            new_user = authenticate(username=form.cleaned_data.get('username'), 
                                    password=form.cleaned_data.get('password1'))
            login(request, new_user)
            
            # Send welcome message
            send_welcome(new_user)
            send_moderate("New user signed up.", context={'user': new_user})
            
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
            
    page = request.GET.get('page', 1)

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
            elif tab == 'adduser':
                form = forms.AddUserForm(request.POST)
            elif tab == 'register':
                form = forms.RegisterUserForm(request, data=request.POST)
                request.session['register_selected_members'] = request.POST.getlist('members')
                request.session['register_selected_event'] = request.POST.get('event')
                return redirect(reverse('register-event'))
            if form.is_valid():       
                user = form.save()
                success(request, 'Account Updated Successfully')
                if tab == 'adduser':
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
        send_reminder("Event Registration Pending.", user, context={'event':event})
        
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