from django.contrib import admin
from .forms import *
from .models import Lesson, Lesson_video, Lesson_audio, User_Lesson, Request, Teacher, Course, Blog
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class MovieAdmin(admin.ModelAdmin):
    form = BlogAdminForm




admin.site.register(Lesson)
admin.site.register(Lesson_video)
admin.site.register(Lesson_audio)
admin.site.register(User_Lesson)
admin.site.register(Request)
admin.site.register(Teacher)
admin.site.register(Course)
# Register your models here.
