from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login-user', login_user),
    path('change_email', change_email),
    path('send_request_v', send_request_view),
    path('send_request_vt', send_request_view_teach),
    path('ask_question', ask_question),
    path('price', price),
    path('confidentiality', confidentiality),
    path('oferta', oferta),
    path('ajax_load_lessons/<int:number>', ajax_load_lessons),
    path('ajax_pay_lessons', ajax_pay_lessons),
    path('ajax_load_lessons_videos/<int:number>', ajax_load_lessons_videos),
    path('ajax_load_video/<int:number>', ajax_load_video),
    path('ajax_load_lessons_audios/<int:number>', ajax_load_lessons_audios),
    path('accounts/password_reset/done/', password_reset_done),
    path('accounts/reset/done/', password_reset_complete),
    path('dashboard', dashboard),
    path('logout', loggout),
    path('courses', courses),
    path('blog/<int:number>', blog),
    path('video/<int:number>', video),
    path('video-constructor/<int:number>', video_constructor),
    path('video-listening/<int:number>', video_listening),
]
