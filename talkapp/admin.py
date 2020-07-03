from django.contrib import admin
from .models import UserAdditionals, Lessons, Video_Courses, Audio_Courses

admin.site.register(UserAdditionals)
admin.site.register(Lessons)
admin.site.register(Video_Courses)
admin.site.register(Audio_Courses)
# Register your models here.
