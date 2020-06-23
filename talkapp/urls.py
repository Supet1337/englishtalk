from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('profile', profile),
    path('courses', courses),
    path('about', about),
]
