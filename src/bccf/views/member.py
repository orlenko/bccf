from cartridge.shop.models import Category, Product, Order, ProductVariation
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from bccf.forms import ProfileForm
from cartridge.shop.utils import recalculate_cart
from cartridge.shop import checkout


def profile(request):
    user_profile = request.user.profile
    form = ProfileForm(request.POST, instance=user_profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, 'Your Profile has been successfully updated.')
        return HttpResponseRedirect(request.GET.get('next', '/'))
    context = RequestContext(request, locals())
    return render_to_response('bccf/member_profile.html', {}, context_instance=context)


def membership(request, slug):
    slugs = [slug, 'membership/%s' % slug]
    the_category = None
    for categ in Category.objects.all():
        if categ.slug in slugs:
            the_category = categ
            break
    if not the_category:
        messages.warning(request, 'Sorry, could not find membership types matching "%s"' % slug)
        return HttpResponseRedirect()

    if request.method == 'POST':
        variation_id = int(request.POST.get('variation_id'))
        variation = ProductVariation.objects.get(id=variation_id)
        request.cart.add_item(variation, 1)
        recalculate_cart(request)
        messages.info(request, "Your membership has been added to cart")
        request.session['aftercheckout'] = request.GET.get('next', '/')
        if request.cart.total_price():
            return redirect("shop_checkout")
        else:
            # For free membership, just fake the purchase process
            order = Order.objects.create()
            order.setup(request)
            order.complete(request)
            request.user.profile.membership_order = order
            request.user.profile.save()
            checkout.send_order_email(request, order)
            return redirect("shop_complete")

    context = RequestContext(request, locals())
    return render_to_response('bccf/member_membership.html', {}, context_instance=context)


def membership_upgrade(request, product_id):
    '''This view handles these scenarios:
     - A purchase of a paid membership by a holder of a free membership
         - this is equivalent to the membership purchase by new members,
           except we'll need to clean up the free membership at the end.
     - A renewal of the same type of membership
     - An upgrade to a higher-tier membership
     - A downgrade to a lower-tier membership.
    '''
    variation = ProductVariation.objects.get(product_id)
    current = //