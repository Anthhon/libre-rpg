from django import forms
from apps.campaigns.models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'cover_image']
        widgets = {
                'cover_image': forms.ClearableFileInput(attrs={
                    'class': 'cover-input',
                    'accept': 'image/*'
                    }),
                'name': forms.TextInput(attrs={
                    'class': 'field-input',
                    'placeholder': 'A Maldição do Rei Morto...',
                    'maxlength': 32,
                    }),
                'description': forms.Textarea(attrs={
                    'class': 'field-textarea',
                    'placeholder': 'Uma breve descrição da aventura...',
                    'maxlength': 128,
                    'rows': 3,
                    'id': 'id_description',
                    }),
                }
