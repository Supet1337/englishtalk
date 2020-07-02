from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    email = forms.EmailField()
    first_name = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
