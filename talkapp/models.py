from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField

def video_directory_path(instance, filename):
    return 'lessons/lesson_{0}/videos/{1}'.format(instance.lesson.id, filename)

def audio_directory_path(instance, filename):
    return 'lessons/lesson_{0}/audio/{1}'.format(instance.lesson.id, filename)

class Teacher(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=64)
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)

    LESSON_TIME_CHOISES = [
        (True, '60 минут'),
        (False, '45 минут')
    ]

    lesson_time = models.BooleanField(choices=LESSON_TIME_CHOISES,default=False)

    def __str__(self):
        return self.name

# Create your models here.
class Lesson(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    docx_url = models.URLField()
    name = models.CharField(max_length=64)
    date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    video_chat = models.CharField(max_length=16, default=get_random_string(length=16))

    def __str__(self):
        return self.name

    def json(self):
        return {
            'docx_url': self.docx_url,
            'name': self.name,
            'id': self.id,
            }
    def get_lesson_videos(self):
        return Lesson_video.objects.filter(lesson_id=self.id)
    def get_lesson_audios(self):
        return Lesson_audio.objects.filter(lesson_id=self.id)


class Lesson_video(models.Model):
    name = models.CharField(max_length=64)
    video_url = models.FileField(upload_to=video_directory_path, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json(self):
        return {
            'video_url': self.video_url.url,
            'video_id': self.id,
            'video_name': self.name,
            'lesson_id': self.lesson.id,
            }

class Lesson_audio(models.Model):
    name = models.CharField(max_length=64)
    audio_url = models.FileField(upload_to=audio_directory_path, blank=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json(self):
        return {
            'audio_url': self.audio_url.url,
            'audio_name': self.name,
            }

class Request(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

class Blog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
