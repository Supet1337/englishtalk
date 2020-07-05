from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAdditionals

class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # do not require password confirmation


