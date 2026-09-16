from django import forms
from apps.campaigns.models import Campaign

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
