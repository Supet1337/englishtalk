from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('login-user', login_user),
    path('accounts/login/', redirect_login),
    path('check-email',check_email),
    path('change_email', change_email),
    path('homework-upload', homework_upload),
    path('update-profile-picture', update_profile_picture),
    path('delete-profile-picture', delete_profile_picture),
    path('send_request_v', send_request_view),
    path('send_request_vt', send_request_view_teach),
    path('change-info', change_info),
    path('change-password', change_password),
    path('change-additional-info', change_additional_info),
    path('save-blog/<int:number>',save_blog),
    path('ask_question', ask_question),
    path('add_word_tape', add_word_tape),
    path('price', price),
    path('confidentiality', confidentiality),
    path('oferta', oferta),
    path('ajax_load_lessons/<int:number>', ajax_load_lessons),
    path('ajax_load_homework/<int:number>', ajax_load_homework),
    path('ajax_delete_word/<int:number>', ajax_delete_word),
    path('ajax_pay_lessons', ajax_pay_lessons),
    path('ajax_load_lessons_videos/<int:number>', ajax_load_lessons_videos),
    path('ajax_load_video/<int:number>', ajax_load_video),
    path('ajax_load_lessons_audios/<int:number>', ajax_load_lessons_audios),
    path('ajax_load_homework_audios/<int:number>', ajax_load_homework_audios),
    path('ajax_load_homework_videos/<int:number>', ajax_load_homework_videos),
    path('ajax_load_homework_files/<int:number>', ajax_load_homework_files),
    path('accounts/password_reset/done/', password_reset_done),
    path('accounts/reset/done/', password_reset_complete),
    path('dashboard/account', dashboard_account),
    path('dashboard/lk', dashboard_lk),
    path('dashboard/platform', dashboard_platform),
    path('dashboard/schedule', dashboard_schedule),
    path('dashboard/homework', dashboard_homework),
    path('dashboard/tape', dashboard_tape),
    path('dashboard/courses', dashboard_courses),
    path('dashboard/blog/<int:number>', dashboard_blog),
    path('logout', loggout),
    path('courses', courses),
    path('blogs', blogs),
    path('blog/<int:number>', blog),
    path('video/<int:number>', video),
    path('video-constructor/<int:number>', video_constructor),
    path('video-listening/<int:number>', video_listening),
    path('check_aswer/<int:number>', check_answer)
]
