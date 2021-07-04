"""adapter.py"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
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
        user_add.birthday = user.socialaccount_set.filter(provider='vk')[0].extra_data['bdate']

        room.name = roomName
        room.student = user

        # user_add.image = user.socialaccount_set.filter(provider='vk')[0].extra_data['photo']
        user_add.save()
        room.save()
