from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'field-input',
            'placeholder': 'Seu nome de usuário...',
            'autocomplete': 'off',
            'maxlength': '150',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'field-input',
            'placeholder': 'Sua senha secreta...',
            'autocomplete': 'current-password',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default labels
        self.fields['username'].label = ''
        self.fields['password'].label = ''
