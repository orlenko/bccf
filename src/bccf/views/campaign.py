import logging
log = logging.getLogger(__name__)

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bccf.models import Campaign
from bccf.forms import CampaignForm

@login_required
def create(request):
    form = CampaignForm(initial={'user':request.user, 'by_user':True, 'status':1, 'approve':False})
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign successfully created')
            return HttpResponseRedirect(form.instance.edit_url())
        else:
            messages.error(request, 'Please fix the errors below')
    title = 'Create Campaign'
    context = RequestContext(request, locals())
    return render_to_response('bccf/campaign_create.html', {}, context)   
   
@login_required 
def edit(request, slug):
    profile = request.user.profile
    
    if not Campaign.objects.filter(slug=slug, user=profile).exists():
        return HttpResponseRedirect('/')
        
    campaign = Campaign.objects.get(slug=slug)
    form = CampaignForm(instance=campaign)
    title = 'Edit %s' % campaign.title    
    
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign successfully updated')    
            title = 'Edit %s' % form.instance.title
        else:
            messages.error(request, 'Please fix the errors below')
       
    context = RequestContext(request, locals())
    return render_to_response('bccf/campaign_create.html', {}, context)