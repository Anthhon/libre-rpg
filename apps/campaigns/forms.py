from django import forms
from apps.campaigns.models import Campaign
from apps.core.models import Profile

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'cover_image']
        widgets = {
                'cover_image': forms.ClearableFileInput(attrs={
                    'accept': 'image/*'
                    }),
                'name': forms.TextInput(attrs={
                    'placeholder': 'Nome da campanha',
                    'maxlength': 32,
                    }),
                'description': forms.Textarea(attrs={
                    'placeholder': 'Breve descrição da campanha...',
                    'maxlength': 128,
                    'rows': 3,
                    }),
                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampaignAddPlayerForm(forms.Form):
    players = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.none(),  # queryset set in __init__
        widget=forms.CheckboxSelectMultiple,
        label="Jogadores",
        error_messages={'required': "Selecione ao menos um jogador."},
    )

    def __init__(self, *args, campaign, **kwargs):
        super().__init__(*args, **kwargs)
        self.campaign = campaign
        self.fields['players'].queryset = (
                Profile.objects
                .select_related('user')  # __str__ use user.username, avoid N+1
                .exclude(pk__in=campaign.masters.values('pk'))
                .exclude(pk__in=campaign.players.values('pk'))
                .order_by('user__username')
                )

    def save(self):
        players = self.cleaned_data['players']
        self.campaign.players.add(*players)
        return players
