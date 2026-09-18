from django.shortcuts import render, redirect, get_object_or_404
from apps.core.views import get_user_profile
from django.contrib.auth.decorators import login_required
from apps.campaigns.models import Campaign
from django.contrib.auth import login
from apps.campaigns.forms import CampaignForm
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.views.decorators.http import require_POST

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
                messages.error(request, f'Erro ao tentar criar a campanha: {str(e)}')
                return render(request, "campaign_creator.html", {
                    'profile': profile,
                    'new_campaign_form': form,
                    })

            messages.success(request, f'Campanha \'{campaign.name}\' criada com sucesso!')
            return redirect('campaign_list')
        else:
            messages.error(request, f'Por favor corrija os erros abaixo.')
    else:
        form = CampaignForm()

    return render(request, "campaign_creator.html", {
        'profile': profile,
        'new_campaign_form': form,
        })


@login_required(login_url="login")
def campaign_player_remove(request, campaign_id, player_id):
    """Remove player with given ID from campaign"""
    profile = get_user_profile(request.user)
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    # Only masters can remove players
    if not campaign.masters.filter(pk=profile.pk).exists():
        messages.error(request, 'Somente os mestres de uma campanha podem remover jogadores.')
        return redirect('players_list', campaign.pk)

    # Player must belong to this campaign
    player = campaign.players.filter(pk=player_id).first()
    if player is None:
        messages.error(request, 'Jogador não encontrado nesta campanha.')
        return redirect('players_list', campaign.pk)
    
    # Remove o jogador da campanha
    campaign.players.remove(player)
    messages.success(request, f'{player} removido da campanha.')
    return redirect('players_list', campaign.pk)
