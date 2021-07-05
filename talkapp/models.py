import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import dateformat
from django.conf import settings
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField


def video_directory_path(instance, filename):
    return 'lessons/lesson_{0}/videos/{1}'.format(instance.lesson.id, filename)

def video_homework_directory_path(instance, filename):
    return 'homeworks/homework_{0}/videos/{1}'.format(instance.homework.id, filename)

def audio_homework_directory_path(instance, filename):
    return 'homeworks/homework_{0}/audios/{1}'.format(instance.homework.id, filename)

def audio_directory_path(instance, filename):
    return 'lessons/lesson_{0}/audio/{1}'.format(instance.lesson.id, filename)


def teacher_image_directory_path(instance, filename):
    return 'lessons/teacher_{0}/{1}'.format(instance.user.id, filename)


def blog_image_directory_path(instance, filename):
    return 'blogs/blog_{0}/{1}'.format(instance.id, filename)


def video_image_directory_path(instance, filename):
    return 'Videos/video_{0}/{1}'.format(instance.id, filename)


class Teacher(models.Model):
    class Meta:
        verbose_name_plural = "Учителя"

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(upload_to=teacher_image_directory_path, blank=True, verbose_name='Фотография')

    def __str__(self):
        return self.user.username


class DefaultCourse(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название курса')

    LEVEL_CHOICES = [
        ('Elementary', 'Elementary'),
        ('Begginer', 'Begginer'),
        ('Intermediate', 'Intermediate'),
        ('Pre-Intermediate', 'Pre-Intermediate'),
        ('Upper-Intermediate', 'Upper-Intermediate')
    ]

    MODULE_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    ]

    level = models.CharField(max_length=64, verbose_name='Уровень подготовки', choices=LEVEL_CHOICES)
    module = models.IntegerField('Модуль', choices=MODULE_CHOICES)

    class Meta:
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


# Create your models here.
class DefaultLesson(models.Model):
    course = models.ForeignKey(to=DefaultCourse, on_delete=models.CASCADE, verbose_name='Курс')
    name = models.CharField(max_length=64, verbose_name='Название урока')
    docx_url = models.URLField(verbose_name='Ссылка на документ с уроком')

    class Meta:
        verbose_name_plural = "Материалы урока"

    def __str__(self):
        return self.name

    def get_lesson_videos(self):
        return Lesson_video.objects.filter(lesson_id=self.id)

    def get_lesson_audios(self):
        return Lesson_audio.objects.filter(lesson_id=self.id)


class UserCourse(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Ученик')
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name='Учитель')

    class Meta:
        verbose_name_plural = "Ученик и его курс"

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
    course_type = models.CharField(choices=TYPE_CHOISES, max_length=64, verbose_name='Тип курса')


class UserLesson(models.Model):
    user_course = models.ForeignKey(to=UserCourse, on_delete=models.CASCADE, verbose_name='В составе курса')
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE, verbose_name='Материалы урока')
    docx_url_copy = models.URLField(verbose_name='Ссылка на копию документа с уроком')
    date = models.DateTimeField(verbose_name='Дата и время урока')
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
    name = models.CharField(max_length=64, verbose_name='Название видеофайла')
    video_url = models.FileField(upload_to=video_directory_path, blank=True, verbose_name='Видеофайл')
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE, verbose_name='Урок')

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
    name = models.CharField(max_length=64, verbose_name='Название аудиофайла')
    audio_url = models.FileField(upload_to=audio_directory_path, blank=True, verbose_name='Аудиофайл')
    lesson = models.ForeignKey(to=DefaultLesson, on_delete=models.CASCADE, verbose_name='Урок')

    def __str__(self):
        return self.name

    def json(self):
        return {
            'audio_url': self.audio_url.url,
            'audio_name': self.name,
            'audio_id': self.id
        }


class Blog(models.Model):
    class Meta:
        verbose_name_plural = "Блоги"

    author = models.CharField(max_length=50, verbose_name='Автор')
    content = models.CharField(max_length=10000, verbose_name='Контент')
    description = models.CharField(max_length=300, verbose_name='Описание')
    title_picture = models.ImageField(upload_to=blog_image_directory_path, blank=True, verbose_name='Превью')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, verbose_name='Заголовок')


class UserAdditional(models.Model):
    class Meta:
        verbose_name_plural = "Дополнительная информация о пользователях"

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = PhoneNumberField(verbose_name='Телефон', blank=True)
    video_chat = models.CharField(max_length=32, verbose_name='Код личного видеочата')
    paid_lessons = models.IntegerField(verbose_name='Кол-во оплаченных занятий', default=1)
    birthday = models.DateField(verbose_name='Дата рождения', default=datetime.date.today(),blank=True)
    saved_blogs = models.TextField(max_length=1024, blank=True)
    LESSON_TIME_CHOISES = [
        (True, '60 минут'),
        (False, '45 минут')
    ]

    lesson_time = models.BooleanField(choices=LESSON_TIME_CHOISES, default=False,
                                      verbose_name='Продолжительность уроков')


class VideoCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название категории')

    class Meta:
        verbose_name_plural = "Категории видео"

    def __str__(self):
        return self.name

    def get_videos(self):
        return VideoPractise.objects.filter(category=self)


class VideoPractise(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    video_url = models.CharField(max_length=32, verbose_name='Ссылка на видео')
    name = models.CharField(max_length=100, verbose_name='Название')
    picture = models.ImageField(upload_to=video_image_directory_path, verbose_name='Превью')
    category = models.ForeignKey(to=VideoCategory, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name_plural = "Видеопрактика"

    def get_words(self):
        return VideoPractiseWord.objects.filter(video_practise=self)


class VideoPractiseWord(models.Model):
    video_practise = models.ForeignKey(to=VideoPractise, on_delete=models.CASCADE, verbose_name='Видеопрактика')
    word = models.CharField(max_length=100, verbose_name='Слово на английском')
    translate = models.CharField(max_length=100, verbose_name='Перевод')


class VideoPractiseConstructor(models.Model):
    video_practise = models.ForeignKey(to=VideoPractise, on_delete=models.CASCADE, verbose_name='Видеопрактика')
    video_start_time = models.TimeField(verbose_name='Время начала фрагмента из видео')
    video_end_time = models.TimeField(verbose_name='Время конца фрагмента из видео')
    answer = models.CharField(max_length=100, verbose_name='Правильный ответ на английском')
    answer_translate = models.CharField(max_length=100, verbose_name='Перевод ответа')

    def get_possible_answers(self):
        l = list(self.answer.split())
        random.shuffle(l)
        return l

    def get_start_seconds(self):
        return int(datetime.timedelta(hours=self.video_start_time.hour, minutes=self.video_start_time.minute,
                                      seconds=self.video_start_time.second).total_seconds())

    def get_end_seconds(self):
        return int(datetime.timedelta(hours=self.video_end_time.hour, minutes=self.video_end_time.minute,
                                      seconds=self.video_end_time.second).total_seconds())


class VideoPractiseListening(models.Model):
    video_practise = models.ForeignKey(to=VideoPractise, on_delete=models.CASCADE, verbose_name='Видеопрактика')
    video_start_time = models.TimeField(verbose_name='Время начала фрагмента из видео')
    video_end_time = models.TimeField(verbose_name='Время конца фрагмента из видео')
    answer = models.CharField(max_length=100, verbose_name='Правильный ответ на английском')
    answer_translate = models.CharField(max_length=100, verbose_name='Перевод ответа')

    def get_answer(self):
        l = list(self.answer.split())
        r = random.randint(0, len(l) - 1)
        first = ''
        second = ' '
        for a in l[:r]:
            first += a + ' '
        for a in l[r + 1:len(l)]:
            second += a + ' '
        second = second[:-1]
        res1 = [[first], [second]]
        res = [res1]
        return res

    def get_start_seconds(self):
        return int(datetime.timedelta(hours=self.video_start_time.hour, minutes=self.video_start_time.minute,
                                      seconds=self.video_start_time.second).total_seconds())

    def get_end_seconds(self):
        return int(datetime.timedelta(hours=self.video_end_time.hour, minutes=self.video_end_time.minute,
                                      seconds=self.video_end_time.second).total_seconds())


class ChatRoom(models.Model):
    name = models.CharField(max_length=32)
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def get_messages(self):
        return ChatMessage.objects.filter(room=self)


class ChatMessage(models.Model):
    message = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE)


class Tape(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    translate = models.CharField(max_length=60)
    word = models.CharField(max_length=60)


class Homework(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Ученик')
    homework_name = models.CharField(max_length=60, verbose_name='Название дз')
    picture = models.ImageField(upload_to=blog_image_directory_path, blank=True, verbose_name='Баннер')
    exercise = models.CharField(max_length=360, verbose_name='Формулировка задания')
    exercise_content = models.CharField(max_length=360, verbose_name='Текст задания')

    answer = models.CharField(max_length=1360, verbose_name='Ответ', blank=True)
    correct_answer = models.CharField(max_length=1360, verbose_name='Правильный ответ', blank=True)
    is_completed = models.BooleanField(verbose_name='Задание выполнено верно', default=False)

    def get_homework_videos(self):
        return Homework_video.objects.filter(homework_id=self.id)

    def get_homework_audios(self):
        return Homework_audio.objects.filter(homework_id=self.id)

    def json(self):
        return {
            'homework_picture': self.picture.url,
            'homework_exercise': self.exercise,
            'homework_name': self.homework_name,
            'homework_id': self.id,
            'homework_correct_answer': self.correct_answer,
            'homework_exercise_content':  self.exercise_content,
            'homework_is_completed':  self.is_completed
        }




class Homework_video(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название видеофайла')
    video_url = models.FileField(upload_to=video_homework_directory_path, blank=True, verbose_name='Видеофайл')
    homework = models.ForeignKey(to=Homework, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    def json(self):
        return {
            'video_url': self.video_url.url,
            'video_id': self.id,
            'video_name': self.name,
            'homework_id': self.homework.id,
        }


class Homework_audio(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название аудиофайла')
    audio_url = models.FileField(upload_to=audio_homework_directory_path, blank=True, verbose_name='Аудиофайл')
    homework = models.ForeignKey(to=Homework, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    def json(self):
        return {
            'audio_url': self.audio_url.url,
            'audio_name': self.name,
            'audio_id': self.id
        }
