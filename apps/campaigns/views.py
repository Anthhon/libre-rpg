from django.shortcuts import render, redirect
from apps.core.views import context_get
from django.contrib.auth.decorators import login_required
from apps.campaigns.models import Campaign
from django.contrib.auth import login
from apps.campaigns.forms import CampaignForm
from django.contrib import messages
from django.db import models
from django.db.models import Q

# Create your views here.
@login_required(login_url="login")
def campaign_list_render(request):
    context = context_get(request, 'campaign_list')
    user = request.user

    # Get only the campaigns related to the user, with prefetched data
    # for faster iterations on masters and players info in the templates. 
    campaigns = Campaign.objects.filter(
        models.Q(masters=user) | models.Q(players=user),
        active=True
        ).order_by('-created_at').prefetch_related('masters', 'players').distinct()

    return render(request, "campaign_list.html", {
        'context': context,
        'campaigns': campaigns,
        })


@login_required(login_url="login")
def campaign_creator_render(request):
    context = context_get(request, 'campaign_creator')
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                campaign = form.save(commit=False)  # Doesn't save yet
                # Set the current user as the only master
                campaign.save()
                campaign.masters.add(request.user)
                campaign.save()
            except Exception as e:
                messages.error(request, f'Error creating campaign: {str(e)}')
                return render(request, "campaign_creator.html", {
                    'context': context,
                    'new_campaign_form': form,
                    })

            messages.success(request, f'Campaign {campaign.name} created successfully!')
            return redirect('campaign_list')
        else:
            messages.error(request, f'Please correct the errors below.')
    else:
        form = CampaignForm()

    return render(request, "campaign_creator.html", {
        'context': context,
        'new_campaign_form': form,
        })
