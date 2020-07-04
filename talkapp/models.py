from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField

def video_directory_path(instance, filename):
    return 'lessons/lesson_{0}/videos/{1}'.format(instance.lesson.id, filename)

def audio_directory_path(instance, filename):
    return 'lessons/lesson_{0}/audio/{1}'.format(instance.lesson.id, filename)

class UserAdditionals(models.Model):
    """
    Модель для дополнительных настроек пользователя.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

# Create your models here.
class Lesson(models.Model):
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
    def get_lesson_videos(self):
        return Lesson_video.objects.filter(lesson_id=self.id)
    def get_lesson_audios(self):
        return Lesson_audio.objects.filter(lesson_id=self.id)


class Lesson_video(models.Model):
    video_url = models.FileField(upload_to=video_directory_path, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    def json(self):
        return {
            'video_url': self.video_url.url
            }

class Lesson_audio(models.Model):
    audio_url = models.FileField(upload_to=audio_directory_path, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    def json(self):
        return {
            'audio_url': self.audio_url.url
            }
