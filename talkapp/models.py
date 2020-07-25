import datetime

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

def teacher_image_directory_path(instance, filename):
    return 'lessons/teacher_{0}/{1}'.format(instance.user.id, filename)

class Teacher(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=teacher_image_directory_path, blank=True)
    def __str__(self):
        return self.user.username


class DefaultCourse(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# Create your models here.
class DefaultLesson(models.Model):
    course = models.ForeignKey(to=DefaultCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    docx_url = models.URLField()

    def __str__(self):
        return self.name

    def get_lesson_videos(self):
        return Lesson_video.objects.filter(lesson_id=self.id)
    def get_lesson_audios(self):
        return Lesson_audio.objects.filter(lesson_id=self.id)

class UserCourse(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)

    LESSON_TIME_CHOISES = [
        (True, '60 минут'),
       (False, '45 минут')
    ]
    TYPE_CHOISES = [
        ('Подготовка к IELTS', 'Подготовка к IELTS'),
        ('Собеседование', 'Собеседование'),
        ('Английский для IT', 'Английский для IT'),
        ('Английский для любого уровня', 'Английский для любого уровня'),
        ('Английский для путешествий', 'Английский для путешествий'),
        ('Бизнес Английский', 'Бизнес Английский'),
        ('Подготовка к ЕГЭ', 'Подготовка к ЕГЭ'),
        ('Английский для инженеров', 'Английский для инженеров'),
        ('Английский для подростков', 'Английский для подростков'),
        ('Английский детям', 'Английский детям'),
        ('Говорим свободно', 'Говорим свободно'),
        ('Персональный курс', 'Персональный курс'),
    ]
    course_type = models.CharField(choices=TYPE_CHOISES,max_length=64)
    lesson_time = models.BooleanField(choices=LESSON_TIME_CHOISES,default=False)


class UserLesson(models.Model):
    user_course = models.ForeignKey(to=UserCourse, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE)
    docx_url_copy = models.URLField()
    date = models.DateTimeField()
    date_end = models.DateTimeField(default=datetime.datetime.now())
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson.name

    def json(self):
        return {
            'docx_url_copy': self.docx_url_copy,
            'name': self.lesson.name,
            'student_email': self.user_course.student.email
            }


class Lesson_video(models.Model):
    name = models.CharField(max_length=64)
    video_url = models.FileField(upload_to=video_directory_path, blank=True)
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE)

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
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json(self):
        return {
            'audio_url': self.audio_url.url,
            'audio_name': self.name,
            }

class UserAdditional(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    video_chat = models.CharField(max_length=32, default=get_random_string(length=32))

class Blog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
