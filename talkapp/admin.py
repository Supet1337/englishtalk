from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import *
import nested_admin
from .models import DefaultLesson, Lesson_video, Lesson_audio, UserAdditional, Teacher, DefaultCourse,\
    Blog, UserCourse, UserLesson, VideoPractiseWord, VideoPractise, VideoPractiseConstructor,VideoPractiseListening,\
    VideoCategory, ChatRoom, ChatMessage, Tape, Homework, Homework_video, Homework_audio
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

class InLineVideoLesson(admin.StackedInline):
    model = Lesson_video
    extra = 0

class InLineAudioLesson(admin.StackedInline):
    model = Lesson_audio
    extra = 0

class InLineVideoHomework(admin.StackedInline):
    model = Homework_video
    extra = 0

class InLineAudioHomework(admin.StackedInline):
    model = Homework_audio
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

class InLineWord(admin.StackedInline):
    model = VideoPractiseWord
    extra = 0

class InLineConstructor(admin.StackedInline):
    model = VideoPractiseConstructor
    extra = 0

class InLineListening(admin.StackedInline):
    model = VideoPractiseListening
    extra = 0

@admin.register(DefaultCourse)
class DefaultCourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineDefaultLesson]
    list_display = ('name','level','module')
    list_filter = ('name','level','module')
    search_fields = ['name','level','module']

@admin.register(UserCourse)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [InLineUserLesson]
    raw_id_fields = ("student","teacher")
    list_display = ('student_name','teacher_name','course_type')
    search_fields = ['student__first_name', 'teacher__first_name', 'course_type']
    list_filter = ('course_type',)
    def student_name(self,obj):
        return obj.student.first_name

    def teacher_name(self,obj):
        return obj.teacher.user.first_name

@admin.register(DefaultLesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [InLineVideoLesson,InLineAudioLesson]
    list_display = ('name','course','course_level','course_module','docx_url')
    list_filter = ('course','course__level','course__module')
    search_fields = ['name','course__name','course__level','course__module','docx_url']
    def course_level(self,obj):
        return obj.course.level
    def course_module(self,obj):
        return obj.course.module

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
    inlines = [InLineWord,InLineConstructor,InLineListening]
    raw_id_fields = ('author',)
    list_display = ('name','category', 'author_name', 'video_url')
    search_fields = ['author__first_name', 'name','category']
    def author_name(self,obj):
        return obj.author.first_name


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    inlines = [InLineAudioHomework,InLineVideoHomework]


admin.site.register(VideoCategory)
admin.site.register(ChatRoom)
admin.site.register(Tape)
admin.site.unregister(Group)
