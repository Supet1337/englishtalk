from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAdditional

class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = UserAdditional
        fields = ['image']

