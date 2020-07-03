from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField

def video_directory_path(instance, filename):
    """
    Функция возврата пути изображения для профиля

    :param instance: Пример
    :param filename: Имя файла
    :return: Возвращает путь к файлу
    """
    return 'lesson/video/id_{0}/{1}'.format(instance.lessons.id, filename)

def audio_directory_path(instance, filename):
    """
    Функция возврата пути изображения для профиля

    :param instance: Пример
    :param filename: Имя файла
    :return: Возвращает путь к файлу
    """
    return 'lesson/audio/id_{0}/{1}'.format(instance.lessons.id, filename)

class UserAdditionals(models.Model):
    """
    Модель для дополнительных настроек пользователя.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

# Create your models here.
class Lessons(models.Model):
    docx_url = models.URLField()
    name = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now_add=True)

    def json(self):
        datef = dateformat.format(self.date, settings.DATE_FORMAT)
        return {
            'docx_url': self.docx_url,
            'name': self.name,
            'date': str(datef),
            'id': self.id,
            }


class Video_Courses(models.Model):
    video_url = models.FileField(upload_to=video_directory_path, blank=True)
    lessons = models.ForeignKey(to=Lessons, on_delete=models.CASCADE)

class Audio_Courses(models.Model):
    audio_url = models.FileField(upload_to=audio_directory_path, blank=True)
    lessons = models.ForeignKey(to=Lessons, on_delete=models.CASCADE)
