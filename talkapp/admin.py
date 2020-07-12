from django.contrib import admin
from .models import Lesson, Lesson_video, Lesson_audio, User_Lesson, Request, Teacher, Course

admin.site.register(Lesson)
admin.site.register(Lesson_video)
admin.site.register(Lesson_audio)
admin.site.register(User_Lesson)
admin.site.register(Request)
admin.site.register(Teacher)
admin.site.register(Course)
# Register your models here.
