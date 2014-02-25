import logging
from uuid import uuid4

from cartridge.shop import checkout
from cartridge.shop.models import (Category, Order, ProductVariation,
    DiscountCode)
from cartridge.shop.utils import recalculate_cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from bccf.util.memberutil import get_upgrades, require_any_membership
from bccf.forms import AddUserForm, AddExistingUserForm, DelMember, AddUsersForm, ReqProgram
from bccf.models import ProgramRequest

log = logging.getLogger(__name__)


@login_required
def profile(request):
    user = request.user
    user_profile = user.profile
    order = user_profile.membership_order
    membership = user_profile.membership_product_variation
    expiration = user_profile.membership_expiration_datetime
    upgrades = get_upgrades(membership)
    add_users_form = AddUsersForm(initial=dict(organization=user.pk))
    add_existing_user_form = AddExistingUserForm(initial=dict(organization=user.pk))
    program_requests = ProgramRequest.objects.filter(user=user)
    if 'addmembers' in request.session:
        try:
            new_users, new_user_errors = request.session.pop('addmembers')
            feedback = {
                'new_users': new_users,
                'new_user_errors': new_user_errors
            }
        except:
            pass

    context = RequestContext(request, locals())
    return render_to_response('bccf/membership/member_profile.html', {}, context_instance=context)


@login_required
def membership(request, slug):
    slugs = [slug, 'membership/%s' % slug]
    the_category = None
    for categ in Category.objects.all():
        if categ.slug in slugs:
            the_category = categ
            break
    if not the_category:
        log.debug('Sorry, could not find membership types matching "%s"' % slug)
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        variation_id = int(request.POST.get('variation_id'))
        variation = ProductVariation.objects.get(id=variation_id)
        request.cart.add_item(variation, 1)
        recalculate_cart(request)
        messages.success(request, "Your membership has been added to cart")
        request.session['aftercheckout'] = request.GET.get('next', '/')
        if request.cart.total_price():
            return redirect("shop_checkout")
        else:
            # For free membership, just fake the purchase process
            order = Order.objects.create()
            order.setup(request)
            order.complete(request)
            request.user.profile.set_membership_order(order)
            request.user.profile.save()
            checkout.send_order_email(request, order)
            return redirect("shop_complete")

    context = RequestContext(request, locals())
    return render_to_response('bccf/membership/membership.html', {}, context_instance=context)


def membership_upgrade(request, variation_id):
    '''This view handles these scenarios:
     - A purchase of a paid membership by a holder of a free membership
         - this is equivalent to the membership purchase by new members,
           except we'll need to clean up the free membership at the end.
     - A renewal of the same type of membership
     - An upgrade to a higher-tier membership

     For users holding an existing membership, we'll generate a throwaway discount code
     and use it just for this cart.
    '''
    user = request.user
    profile = user.profile
    current_order = profile.membership_order
    current_membership = profile.membership_product_variation
    current_category = current_membership.product.categories.all()[0]
    variation = ProductVariation.objects.get(pk=variation_id)
    new_category = variation.product.categories.all()[0]
    if current_category.pk != new_category.pk:
        # Cannot upgrade between categories
        messages.warning(request, 'Sorry, cannot upgrade from a %s to a %s'
                         % (current_category, new_category))
        return HttpResponseRedirect(reverse('member-profile'))
    discount_amount = profile.remaining_balance
    discount_code = str(uuid4())
    discount = DiscountCode.objects.create(title='[temporary discount for membership upgrade]',
                            active=True,
                            discount_deduct=discount_amount,
                            code=discount_code,
                            min_purchase=0,
                            free_shipping=False)
    discount_code = '%s%s' % (discount.pk, discount_code[:5])
    discount.code = discount_code
    discount.save() # These 3 lines are a hack, to get a discount code shorter than 20 chars
    discount.products.add(variation.product)
    discount.categories.add(current_category)
    log.debug('Adding item to cart: %s' % variation)
    request.cart.add_item(variation, 1)
    log.debug('New cart: %s %s' % (request.cart, request.cart.has_items()))
    request.session['force_discount'] = discount_code
    log.debug('Session variables: %s' % dict(request.session))
    return redirect('shop_checkout')


@require_any_membership
def membership_renew(request):
    return HttpResponseRedirect(
        reverse(
            'member-membership-upgrade',
            kwargs={
                'variation_id': request.user.profile.membership_product_variation.pk
            }
        )
    )


def membership_select(request):
    user = request.user
    if user and user.profile and user.profile.membership_product_variation:
        return HttpResponseRedirect(reverse(profile))
    return render_to_response('bccf/membership/select.html')


def membership_cancel(request):
    user = request.user
    if not user or user.is_anonymous() or not user.profile or not user.profile.membership_product_variation:
        return HttpResponseRedirect(reverse('member-profile'))
    if request.method == 'POST':
        user.profile.request_membership_cancellation()
        messages.success(request,
                         'Your membership cancellation request has been submitted. '
                         'You should receive an email about this. '
                         'We will get back to you as soon as we can.')
        return HttpResponseRedirect('/')
    context = RequestContext(request, locals())
    return render_to_response('bccf/membership/cancel.html', {}, context_instance=context)


def addmember(request):
    form = AddUsersForm(data=request.REQUEST)
    request.session['addmembers'] = form.save(request)
    return HttpResponseRedirect(reverse(profile))


def addexistingmember(request):
    form = AddExistingUserForm(data=request.REQUEST)
    if form.is_valid():
        log.debug('Form is valid - saving %s', form.cleaned_data)
        form.save()
        messages.success(request, 'New member has been successfully added')
    else:
        log.debug('Form invalid: %s' % form)
        messages.error(request, 'Failed to create user. Erros: %s' % form.errors)
    return HttpResponseRedirect(reverse(profile))


def delmember(request):
    form = DelMember(data=request.REQUEST)
    if form.is_valid():
        log.debug('Form is valid - removing %s', form.cleaned_data)
        form.save()
        messages.success(request, 'Member has been removed from the organization')
    else:
        log.debug('Form invalid: %s' % form)
        messages.error(request, 'Failed to remove member. Erros: %s' % form.errors)
    return HttpResponseRedirect(reverse(profile))

def reqprogram(request):
    form = ReqProgram(initial={'user': request.user.pk})
    title = 'Request Program'
    if request.method == 'POST':
        form = ReqProgram(request.POST)
        if form.is_valid():
            form.save()
            return HTTPResponseRedirect(reverse(profile))
    context = RequestContext(request, locals())
    return render_to_response('accounts/account_form.html', {}, context_instance=context)