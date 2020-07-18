from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import *
import nested_admin
from .models import Lesson, Lesson_video, Lesson_audio, Request, Teacher, Course, Blog
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

class InLineVideoLesson(nested_admin.NestedStackedInline):
    model = Lesson_video
    extra = 0

class InLineAudioLesson(nested_admin.NestedStackedInline):
    model = Lesson_audio
    extra = 0

class InLineLesson(nested_admin.NestedStackedInline):
    inlines = [InLineAudioLesson,InLineVideoLesson]
    model = Lesson
    extra = 0
    fields = ('name','docx_url','date')

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineLesson]
    raw_id_fields = ("student","teacher")
    list_display = ('name', 'student_name','teacher_name')
    search_fields = ['name', 'student__username', 'teacher__username']
    list_filter = ('teacher',)
    def student_name(self,obj):
        return "{} {}".format(obj.student.first_name, obj.student.last_name)

    def teacher_name(self,obj):
        return "{} {}".format(obj.teacher.user.first_name, obj.teacher.user.last_name)

#@admin.register(Lesson)
#class LessonAdmin(admin.ModelAdmin):
#    inlines = [InLineVideoLesson,InLineAudioLesson]
#  list_display = ('name','course','docx_url','date')
#    list_filter = ('course',)
#    search_fields = ['name','course__name']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_name', 'teacher_email','phone')
    search_fields = ['user__first_name', 'user__last_name','user__email']
    def teacher_email(self,obj):
        return obj.user.email
    def phone(self,obj):
        return Request.objects.get(user=obj.user).phone_number
    def teacher_name(self,obj):
        return "{} {}".format(obj.user.first_name, obj.user.last_name)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'phone_number')
    search_fields = ['user__first_name', 'user__last_name', 'user__email','phone_number']

    def user_name(self,obj):
        return "{} {}".format(obj.user.first_name, obj.user.last_name)

    def user_email(self,obj):
        return obj.user.email

admin.site.unregister(Group)
# Register your models here.
