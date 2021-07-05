"""adapter.py"""
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.crypto import get_random_string

from .models import UserAdditional, ChatRoom  # pylint:disable=wildcard-import

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Класс SocialAccountAdapter
    """

    def save_user(self, request, sociallogin, form=None):
        """
        Функция сохранения пользователя через socialaccount
        (Добавляет UserAditional к пользователю)

        :param request: запрос
        :param sociallogin: sociallogin
        :param form: Форма
        :return:
        """
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        user_add = UserAdditional()
        room = ChatRoom()
        roomName = get_random_string(length=32)
        user_add.user = user
        user_add.video_chat = roomName
        try:
            s = str(user.socialaccount_set.filter(provider='vk')[0].extra_data['bdate'])
            s = s.split('.')
            s1 = f"{s[2]}-{s[1]}-{s[0]}"
            user_add.birthday = s1
        except:
            pass
        room.name = roomName
        room.student = user
        # user_add.image = user.socialaccount_set.filter(provider='vk')[0].extra_data['photo']
        user_add.save()
        room.save()
