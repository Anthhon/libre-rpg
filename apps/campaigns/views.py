from django.shortcuts import render, redirect
from apps.core.views import get_user_profile
from django.contrib.auth.decorators import login_required
from apps.campaigns.models import Campaign
from django.contrib.auth import login
from apps.campaigns.forms import CampaignForm
from django.contrib import messages
from django.db import models
from django.db.models import Q

@login_required(login_url="login")
def campaign_list_render(request):
    """
    Get only the campaigns related to the user,
    with prefetched data for (masters, players). 
    """
    profile = get_user_profile(request.user)

    campaigns = Campaign.objects.filter(
        models.Q(masters=profile) | models.Q(players=profile),
        active = True,
        ).order_by('-created_at').prefetch_related('masters', 'players')

    return render(request, "campaign_list.html", {
        'profile': profile,
        'campaigns': campaigns,
        })


@login_required(login_url="login")
def campaign_creator_render(request):
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Set the current user as the only master
                campaign = form.save(commit=False)  # Doesn't save yet
                campaign.masters.add(profile)
                campaign.save()
            except Exception as e:
                messages.error(request, f'Error creating campaign: {str(e)}')
                return render(request, "campaign_creator.html", {
                    'profile': profile,
                    'new_campaign_form': form,
                    })

            messages.success(request, f'Campaign {campaign.name} created successfully!')
            return redirect('campaign_list')
        else:
            messages.error(request, f'Please correct the errors below.')
    else:
        form = CampaignForm()

    return render(request, "campaign_creator.html", {
        'profile': profile,
        'new_campaign_form': form,
        })
