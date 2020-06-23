from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('dashboard', dashboard),
    path('courses', courses),
    path('course/<ielts', ielts),
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


]
