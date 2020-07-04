from django.contrib import admin
from .models import UserAdditionals, Lesson, Lesson_video, Lesson_audio

admin.site.register(UserAdditionals)
admin.site.register(Lesson)
admin.site.register(Lesson_video)
admin.site.register(Lesson_audio)
# Register your models here.
