from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import *
import nested_admin
from .models import Lesson, Lesson_video, Lesson_audio, User_Lesson, Request, Teacher, Course, Blog
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.site_header = 'Englishtalk администрирование'

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class MovieAdmin(admin.ModelAdmin):
    form = BlogAdminForm

class InLineVideoLesson(nested_admin.NestedTabularInline):
    model = Lesson_video
    extra = 1

class InLineAudioLesson(nested_admin.NestedTabularInline):
    model = Lesson_audio
    extra = 1

class InLineLesson(nested_admin.NestedTabularInline):
    inlines = [InLineAudioLesson,InLineVideoLesson]
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineLesson]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [InLineVideoLesson,InLineAudioLesson]
    raw_id_fields = ("course",)
    list_display = ('name','course')
    list_filter = ('name','course')
    search_fields = ['name','course__name']

admin.site.register(Lesson_video)
admin.site.register(Lesson_audio)
admin.site.register(User_Lesson)
admin.site.register(Request)
admin.site.register(Teacher)
admin.site.unregister(Group)
# Register your models here.
