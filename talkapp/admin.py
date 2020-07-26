from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import *
import nested_admin
from .models import DefaultLesson, Lesson_video, Lesson_audio, UserAdditional, Teacher, DefaultCourse, Blog, UserCourse, UserLesson, VideoPractiseWord, VideoPractise
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
    raw_id_fields = ('user',)

class InLineVideoLesson(nested_admin.NestedStackedInline):
    model = Lesson_video
    extra = 0

class InLineAudioLesson(nested_admin.NestedStackedInline):
    model = Lesson_audio
    extra = 0

class InLineDefaultLesson(nested_admin.NestedStackedInline):
    inlines = [InLineAudioLesson,InLineVideoLesson]
    model = DefaultLesson
    extra = 0

class InLineUserLesson(nested_admin.NestedStackedInline):
    model = UserLesson
    extra = 0
    fields = ('lesson','docx_url_copy', 'date')
    raw_id_fields = ('lesson',)

class InLineWord(nested_admin.NestedStackedInline):
    model = VideoPractiseWord
    extra = 20

@admin.register(DefaultCourse)
class DefaultCourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineDefaultLesson]
    list_display = ('name',)
    search_fields = ['name']

@admin.register(UserCourse)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineUserLesson]
    raw_id_fields = ("student","teacher")
    list_display = ('student_name','teacher_name','course_type')
    search_fields = ['student__first_name', 'teacher__first_name', 'course_type']
    list_filter = ('teacher','course_type')
    def student_name(self,obj):
        return obj.student.first_name

    def teacher_name(self,obj):
        return obj.teacher.user.first_name

@admin.register(DefaultLesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [InLineVideoLesson,InLineAudioLesson]
    list_display = ('name','course','docx_url')
    list_filter = ('course',)
    search_fields = ['name','course__name','docx_url']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('teacher_name', 'teacher_email','phone')
    search_fields = ['user__first_name', 'user__last_name','user__email']
    def teacher_email(self,obj):
        return obj.user.email
    def phone(self,obj):
        return UserAdditional.objects.get(user=obj.user).phone_number
    def teacher_name(self,obj):
        return obj.user.first_name

@admin.register(UserAdditional)
class UserAdditionals(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'phone_number')
    search_fields = ['user__first_name', 'user__email', 'phone_number']

    def user_name(self,obj):
        return obj.user.first_name

    def user_email(self,obj):
        return obj.user.email

@admin.register(VideoPractise)
class VideoPractiseAdmin(admin.ModelAdmin):
    inlines = [InLineWord]
    raw_id_fields = ('author',)
    list_display = ('name', 'author_name', 'video_url')
    search_fields = ['author__first_name', 'name']
    def author_name(self,obj):
        return obj.author.first_name


admin.site.unregister(Group)
