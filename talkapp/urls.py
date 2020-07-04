from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('register-user', register_user),
    path('login-user', login_user),
    path('ajax_load_lessons/<int:number>', ajax_load_lessons),
    path('dashboard', dashboard),
    path('logout', loggout),
    path('courses', courses),
    path('course/ielts', ielts),
    path('course/interview', interview),
    path('course/freespeaking', freespeaking),
    path('course/it', it),
    path('course/travel', travel),
    path('course/business', business),
    path('course/exam', exam),
    path('course/engineer', engineer),
    path('course/teen', teen),
    path('course/child', child),
    path('course/personally', personally),
    path('course/anylevel', anylevel),
    path('course/grammar', grammar),
    path('blog', blog),
    path('video', video),
]
